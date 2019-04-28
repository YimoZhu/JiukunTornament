"""
//Filename: trading.py
//交易策略：固定形态平移策略
"""

import proto_wrapper as api

import broker_pb2
import grpc
import common_pb2
import broker_pb2_grpc

import threading
from multiprocessing import Process, Queue, Manager
import multiprocessing
#multiprocessing.set_start_method('spawn')
import os
import numpy as np
from time import ctime, sleep, time_ns

import tradingObjects
"""
配置背景参数。
"""

ID = 33
PIN = 'jY0RyHyK9'
CHANNEL_BROKER = grpc.insecure_channel('113.208.112.25:57503') 
CHANNEL_DATA = grpc.insecure_channel('113.208.112.25:57600')

broker_stub = broker_pb2_grpc.BrokerStub(CHANNEL_BROKER)
data_stub = broker_pb2_grpc.MarketDataStub(CHANNEL_DATA)
#//创建客户端

data_stream = data_stub.subscribe(broker_pb2.TraderRequest(trader_id = ID, trader_pin = PIN))
#//获取行情流对象

api.set_stub(broker_stub, data_stub)
api.set_stream(data_stream)
#//设置api客户端

def initStrategy(runtime):
    """
    初始化策略。
    """
    #api.cancel_all()
    #api.close_all_at_market()

    runtime['trader_info_full'] = api.get_trader_full()
    runtime['account_info'] = runtime['trader_info_full'].account
    runtime['order_info'] = tradingObjects.order_info(runtime['trader_info_full'])
    runtime['positions_info'] = tradingObjects.positions_info(runtime['trader_info_full'])

    runtime['TARGETS_MAPPING'] = {'A001.PSE':'A000.PSE','A002.PSE':'A000.PSE','B001.PSE':'B000.PSE','B002.PSE':'B000.PSE'}

    runtime['snapshots_count'] = 0
    runtime['snapshots'] = tradingObjects.snapshots(data_stream.next().instruments)
    
    runtime['isOpen_A001.PSE'] = True
    runtime['isOpen_A002.PSE'] = True
    runtime['isOpen_B001.PSE'] = True
    runtime['isOpen_B002.PSE'] = True

    runtime['loopCount_A001.PSE'] = 0
    runtime['loopCount_A002.PSE'] = 0
    runtime['loopCount_B001.PSE'] = 0
    runtime['loopCount_B002.PSE'] = 0

    runtime['trader_info_count'] = 0

    runtime['net_A001.PSE'] = 0
    runtime['net_A002.PSE'] = 0
    runtime['net_B001.PSE'] = 0
    runtime['net_B002.PSE'] = 0

    runtime['isDigested_A001.PSE'] = 0
    runtime['isDigested_A002.PSE'] = 0
    runtime['isDigested_B001.PSE'] = 0
    runtime['isDigested_B002.PSE'] = 0

def update_trader_info(runtime):    
    """
    更新账户信息。
    """
    #//update trader info
    runtime['trader_info_full'] = broker_stub.get_trader(api.TraderRequest_get_trader_full())
    runtime['account_info'] = runtime['trader_info_full'].account
    runtime['order_info'] = tradingObjects.order_info(runtime['trader_info_full'])
    runtime['positions_info'] = tradingObjects.positions_info(runtime['trader_info_full'])
    runtime['trader_info_count'] += 1

def update_trader_info_looped(runtime):
    """
    循环版本更新账户信息。
    """
    while True:
        runtime['trader_info_full'] = broker_stub.get_trader(api.TraderRequest_get_trader_full())
        runtime['account_info'] = runtime['trader_info_full'].account
        runtime['order_info'] = tradingObjects.order_info(runtime['trader_info_full'])
        runtime['positions_info'] = tradingObjects.positions_info(runtime['trader_info_full'])
        runtime['trader_info_count'] += 1        

def update_snapshots(runtime):
    """
    更新市场信息。
    """
    runtime['snapshots'] = tradingObjects.snapshots(data_stream.next().instruments)
    runtime['isDigested_A001.PSE'] = 0
    runtime['isDigested_A002.PSE'] = 0
    runtime['isDigested_B001.PSE'] = 0
    runtime['isDigested_B002.PSE'] = 0
    runtime['snapshots_count'] += 1

def positions_control(runtime):
    for symbol in ['A001.PSE','B001.PSE','A002.PSE','B002.PSE']:
        positions_info = runtime['positions_info'].info[symbol]
        currLongPos = positions_info['long_positions'].volume + positions_info['long_positions'].locked_volume
        currShortPos = positions_info['short_positions'].volume + positions_info['short_positions'].locked_volume
        #//首先进行市场中性平仓
        if currLongPos - currShortPos > 100:
            response = broker_stub.new_order(api.TraderRequest_new_order(symbol,1,0,currLongPos-currShortPos,is_market=True))
            print(response)
            #//之后进行开平仓控制
            if currShortPos + 100 > 200:
                runtime['isOpen_'+symbol] = False
            else:
                runtime['isOpen_'+symbol] = True
        elif currShortPos - currLongPos > 100:
            response = broker_stub.new_order(api.TraderRequest_new_order(symbol,0,1,currShortPos-currLongPos,is_market=True))
            print(response)
            #//之后进行开平仓控制
            if currLongPos + 100 > 200:
                runtime['isOpen_'+symbol] = False
            else:
                runtime['isOpen_'+symbol] = True

def func_order_info2level(order_info):
    """
    将目前的挂单信息转化为price-volume字典
    """
    buy_level_dict = {}
    sell_level_dict = {}
    for order in order_info.values():
        if order.side == 0:
            try:
                buy_level_dict[order.init_price]['total_volume'] += order.init_volume
                buy_level_dict[order.init_price]['order_IDs'].append(order.order_id)
            except:
                buy_level_dict[order.init_price] = {'total_volume': order.init_volume, 'order_IDs':[]}
        else:
            try:
                sell_level_dict[order.init_price]['total_volume'] += order.init_volume
                sell_level_dict[order.init_price]['order_IDs'].append(order.order_id)
            except:
                sell_level_dict[order.init_price] = {'total_volume': order.init_volume, 'order_IDs':[]}
    return (buy_level_dict,sell_level_dict)


def func_calc_order_delta(curr_level_dict, trm_level_dict):
    """
    根据旧的price-volume字典和目标字典，计算所需的更新操作。
    需要注意买卖方向的一致性，即如果当前字典为bid单字典，那么trm字典也需要为买单字典，
    这样返回值表示需要补上的买单和需要撤掉的买单。
    """
    old = curr_level_dict.copy()
    new_orders = []             #//需要下的单
    cancel_order_id = []        #//需要撤掉的单
    for price, volume in trm_level_dict.items():
        if price in old:
            v_delta = volume - old[price]['total_volume']
            if v_delta > 0 :
                new_orders.append((price, v_delta))
            del old[price]
        else:
            new_orders.append((price, volume))
    #//此时old中剩余的订单需要全部撤单。
    for level in old.values():
        cancel_order_id += level['order_IDs']

    return (new_orders, cancel_order_id)



def trading_A001(runtime):
    """
    price_arr = np.array([[-0.15,-0.13,-0.11,-0.1,-0.07,-0.05],
                          [ 0.05, 0.07, 0.1, 0.11, 0.13, 0.15]])
    volume_arr = np.array([[10,6,2,2,4,6],
                           [6,4,2,2,6,10]])
    """
    price_arr = np.array([[-0.07,-0.05],
                          [ 0.05, 0.07]])
    volume_arr = np.array([[20,24],
                           [24,20]])
    #old_price = 99
    while True:
        if runtime['isDigested_A001.PSE'] == 0:
            snapshot = getattr(runtime['snapshots'],'A001.PSE')
            runtime['isDigested_A001.PSE'] = 1
            last_price = snapshot.last_price
            #if abs(last_price - old_price) >= 0.4:
            #    old_price = last_price
            #    continue
            #old_price = last_price
            bid1 = snapshot.bid_levels[0].price
            ask1 = snapshot.ask_levels[0].price
            if runtime['net_A001.PSE'] == 1:
                buy_trm = dict(zip(price_arr[0,:] + bid1 - 0.02, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + bid1 - 0.02, volume_arr[1,:]))
            elif runtime['net_A001.PSE'] == -1:
                buy_trm = dict(zip(price_arr[0,:] + ask1 + 0.02, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + bid1 + 0.02, volume_arr[1,:]))
            else:
                buy_trm = dict(zip(price_arr[0,:] + last_price, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + last_price, volume_arr[1,:]))            
            curr_buy_order_info, curr_sell_order_info = func_order_info2level(runtime['order_info'].info['A001.PSE'])
            #//计算订单更新
            order_to_cancel = []     
            buy_new_orders, tmp = func_calc_order_delta(curr_buy_order_info, buy_trm)
            order_to_cancel += tmp
            sell_new_orders, tmp = func_calc_order_delta(curr_sell_order_info, sell_trm)
            order_to_cancel += tmp
            buy_new_orders = sorted(buy_new_orders, key = lambda x:x[0], reverse = True)
            sell_new_orders = sorted(sell_new_orders, key = lambda x:x[0], reverse = True)
            #//计算下单
            maxLen = max(len(buy_new_orders), len(sell_new_orders))
            for i in range(maxLen):
                if runtime['isOpen_A001.PSE']:
                    #//开平仓控制
                    try:
                        buy_new_order = buy_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('A001.PSE',0,0,buy_new_order[1],buy_new_order[0]))
                    except:
                        pass
                    try:
                        sell_new_order = sell_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('A001.PSE',1,1,sell_new_order[1],sell_new_order[0]))
                    except:
                        pass
                else:
                    try:
                        buy_new_order = buy_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('A001.PSE',0,1,buy_new_order[1],buy_new_order[0]))
                    except:
                        pass
                    try:
                        sell_new_order = sell_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('A001.PSE',1,0,sell_new_order[1],sell_new_order[0]))
                    except:
                        pass
            #//进行撤单
            for order_id in order_to_cancel:
                broker_stub.cancel_order(api.TraderRequest_cancel_order(order_id))
            print('A001.PSE完成一次操作循环！')
            runtime['loopCount_A001.PSE'] += 1

def trading_A002(runtime):
    """
    price_arr = np.array([[-0.15,-0.13,-0.11,-0.1,-0.07,-0.05],
                          [ 0.05, 0.07, 0.1, 0.11, 0.13, 0.15]])
    volume_arr = np.array([[10,6,2,2,4,6],
                           [6,4,2,2,6,10]])
    """
    price_arr = np.array([[-0.1,-0.07,-0.05],
                          [ 0.05, 0.07,]])
    volume_arr = np.array([[10,12],
                           [12,10]])  
    #old_price = 99
    while True:
        if runtime['isDigested_A002.PSE'] == 0:
            snapshot = getattr(runtime['snapshots'],'A002.PSE')
            runtime['isDigested_A002.PSE'] = 1
            last_price = snapshot.last_price
            #if abs(last_price - old_price) >= 0.4:
            #    old_price = last_price
            #    continue
            #old_price = last_price            
            bid1 = snapshot.bid_levels[0].price
            ask1 = snapshot.ask_levels[0].price
            if runtime['net_A002.PSE'] == 1:
                buy_trm = dict(zip(price_arr[0,:] + bid1 - 0.02, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + bid1 - 0.02, volume_arr[1,:]))
            elif runtime['net_A002.PSE'] == -1:
                buy_trm = dict(zip(price_arr[0,:] + ask1 + 0.02, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + bid1 + 0.02, volume_arr[1,:]))
            else:
                buy_trm = dict(zip(price_arr[0,:] + last_price, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + last_price, volume_arr[1,:]))
            curr_buy_order_info, curr_sell_order_info = func_order_info2level(runtime['order_info'].info['A002.PSE'])
            #//计算订单更新
            order_to_cancel = []
            buy_new_orders, tmp = func_calc_order_delta(curr_buy_order_info, buy_trm)
            order_to_cancel += tmp
            sell_new_orders, tmp = func_calc_order_delta(curr_sell_order_info, sell_trm)
            order_to_cancel += tmp
            buy_new_orders = sorted(buy_new_orders, key = lambda x:x[0], reverse = True)
            sell_new_orders = sorted(sell_new_orders, key = lambda x:x[0], reverse = True)
            #//计算下单
            maxLen = max(len(buy_new_orders), len(sell_new_orders))
            for i in range(maxLen):
                if runtime['isOpen_A002.PSE']:
                    #//开平仓控制
                    try:
                        buy_new_order = buy_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('A002.PSE',0,0,buy_new_order[1],buy_new_order[0]))
                    except:
                        pass
                    try:
                        sell_new_order = sell_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('A002.PSE',1,1,sell_new_order[1],sell_new_order[0]))
                    except:
                        pass
                else:
                    try:
                        buy_new_order = buy_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('A002.PSE',0,1,buy_new_order[1],buy_new_order[0]))
                    except:
                        pass
                    try:
                        sell_new_order = sell_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('A002.PSE',1,0,sell_new_order[1],sell_new_order[0]))
                    except:
                        pass
            #//进行撤单
            for order_id in order_to_cancel:
                broker_stub.cancel_order(api.TraderRequest_cancel_order(order_id))
            print('A002.PSE完成一次操作循环！')
            runtime['loopCount_A002.PSE'] += 1

def trading_B001(runtime):
    """
    price_arr = np.array([[-0.15,-0.13,-0.11,-0.1,-0.07,-0.05],
                          [ 0.05, 0.07, 0.1, 0.11, 0.13, 0.15]])
    volume_arr = np.array([[10,6,2,2,4,6],
                           [6,4,2,2,6,10]])
    """
    price_arr = np.array([[-0.07,-0.05],
                          [ 0.05, 0.07]])
    volume_arr = np.array([[20,24],
                           [24,20]])   
    #old_price = 99
    while True:
        if runtime['isDigested_B001.PSE'] == 0:
            snapshot = getattr(runtime['snapshots'],'B001.PSE')
            runtime['isDigested_B001.PSE'] = 1
            last_price = snapshot.last_price
            #if abs(last_price - old_price) >= 0.4:
            #    old_price = last_price
            #    continue
            #old_price = last_price            
            bid1 = snapshot.bid_levels[0].price
            ask1 = snapshot.ask_levels[0].price
            if runtime['net_B001.PSE'] == 1:
                buy_trm = dict(zip(price_arr[0,:] + bid1 - 0.02, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + bid1 - 0.02, volume_arr[1,:]))
            elif runtime['net_B001.PSE'] == -1:
                buy_trm = dict(zip(price_arr[0,:] + ask1 + 0.02, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + bid1 + 0.02, volume_arr[1,:]))
            else:
                buy_trm = dict(zip(price_arr[0,:] + last_price, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + last_price, volume_arr[1,:]))
            curr_buy_order_info, curr_sell_order_info = func_order_info2level(runtime['order_info'].info['B001.PSE'])
            #//计算订单更新
            order_to_cancel = []
            buy_new_orders, tmp = func_calc_order_delta(curr_buy_order_info, buy_trm)
            order_to_cancel += tmp
            sell_new_orders, tmp = func_calc_order_delta(curr_sell_order_info, sell_trm)
            order_to_cancel += tmp
            buy_new_orders = sorted(buy_new_orders, key = lambda x:x[0], reverse = True)
            sell_new_orders = sorted(sell_new_orders, key = lambda x:x[0], reverse = True)
            #//计算下单
            maxLen = max(len(buy_new_orders), len(sell_new_orders))
            for i in range(maxLen):
                if runtime['isOpen_B001.PSE']:
                    #//开平仓控制
                    try:
                        buy_new_order = buy_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('B001.PSE',0,0,buy_new_order[1],buy_new_order[0]))
                    except:
                        pass
                    try:
                        sell_new_order = sell_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('B001.PSE',1,1,sell_new_order[1],sell_new_order[0]))
                    except:
                        pass
                else:
                    try:
                        buy_new_order = buy_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('B001.PSE',0,1,buy_new_order[1],buy_new_order[0]))
                    except:
                        pass
                    try:
                        sell_new_order = sell_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('B001.PSE',1,0,sell_new_order[1],sell_new_order[0]))
                    except:
                        pass
            #//进行撤单
            for order_id in order_to_cancel:
                broker_stub.cancel_order(api.TraderRequest_cancel_order(order_id))
            print('B001.PSE完成一次操作循环！')
            runtime['loopCount_B001.PSE'] += 1

def trading_B002(runtime):
    """
    price_arr = np.array([[-0.15,-0.13,-0.11,-0.1,-0.07,-0.05],
                          [ 0.05, 0.07, 0.1, 0.11, 0.13, 0.15]])
    volume_arr = np.array([[10,6,2,2,4,6],
                           [6,4,2,2,6,10]])
    """
    price_arr = np.array([[-0.07,-0.05],
                          [ 0.05, 0.07]])
    volume_arr = np.array([[20,24],
                           [24,20]])  
    #old_price = 99                           
    while True:
        if runtime['isDigested_B002.PSE'] == 0:
            snapshot = getattr(runtime['snapshots'],'B002.PSE')
            runtime['isDigested_B002.PSE'] = 1
            last_price = snapshot.last_price
            #if abs(last_price - old_price) >= 0.4:
            #    old_price = last_price
            #    continue
            #old_price = last_price            
            bid1 = snapshot.bid_levels[0].price
            ask1 = snapshot.ask_levels[0].price
            if runtime['net_B002.PSE'] == 1:
                buy_trm = dict(zip(price_arr[0,:] + bid1 - 0.02, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + bid1 - 0.02, volume_arr[1,:]))
            elif runtime['net_B002.PSE'] == -1:
                buy_trm = dict(zip(price_arr[0,:] + ask1 + 0.02, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + bid1 + 0.02, volume_arr[1,:]))
            else:
                buy_trm = dict(zip(price_arr[0,:] + last_price, volume_arr[0,:]))
                sell_trm = dict(zip(price_arr[1,:] + last_price, volume_arr[1,:]))
            curr_buy_order_info, curr_sell_order_info = func_order_info2level(runtime['order_info'].info['B002.PSE'])
            #//计算订单更新
            order_to_cancel = []
            buy_new_orders, tmp = func_calc_order_delta(curr_buy_order_info, buy_trm)
            order_to_cancel += tmp
            sell_new_orders, tmp = func_calc_order_delta(curr_sell_order_info, sell_trm)
            order_to_cancel += tmp
            buy_new_orders = sorted(buy_new_orders, key = lambda x:x[0], reverse = True)
            sell_new_orders = sorted(sell_new_orders, key = lambda x:x[0], reverse = True)
            #//计算下单
            maxLen = max(len(buy_new_orders), len(sell_new_orders))
            for i in range(maxLen):
                if runtime['isOpen_B002.PSE']:
                    #//开平仓控制
                    try:
                        buy_new_order = buy_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('B002.PSE',0,0,buy_new_order[1],buy_new_order[0]))
                    except:
                        pass
                    try:
                        sell_new_order = sell_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('B002.PSE',1,1,sell_new_order[1],sell_new_order[0]))
                    except:
                        pass
                else:
                    try:
                        buy_new_order = buy_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('B002.PSE',0,1,buy_new_order[1],buy_new_order[0]))
                    except:
                        pass
                    try:
                        sell_new_order = sell_new_orders[i]
                        broker_stub.new_order(api.TraderRequest_new_order('B002.PSE',1,0,sell_new_order[1],sell_new_order[0]))
                    except:
                        pass
            #//进行撤单
            for order_id in order_to_cancel:
                broker_stub.cancel_order(api.TraderRequest_cancel_order(order_id))
            print('B002.PSE完成一次操作循环！')
            runtime['loopCount_B002.PSE'] += 1


def func_broker(q_req):
    broker_stub_ind = broker_pb2_grpc.BrokerStub(CHANNEL_BROKER)
    while True:
        req = q_req.get(True)
        if req[0] == 0:
            broker_stub_ind.new_order(req[1])
        else:
            broker_stub_ind.cancel_order(req[1])

if __name__ == '__main__':
    runtime_ = {}
    initStrategy(runtime_)
    print('策略初始化完成！')
    with Manager() as mgr:
        runtime = mgr.dict()
        runtime.update(runtime_)
        """
        q_snapshot_A001 = Queue()
        q_snapshot_A002 = Queue()
        q_snapshot_B001 = Queue()
        q_snapshot_B002 = Queue()
        """
        #//创建请求队列
        #q_req = Queue()

        #//创建并启动分别负责交易四个标的的子进程。
        p_A001 = Process(target = trading_A001, args = (runtime,))
        p_A002 = Process(target = trading_A002, args = (runtime,))
        p_B001 = Process(target = trading_B001, args = (runtime,))
        p_B002 = Process(target = trading_B002, args = (runtime,))
        
        """
        p_broker1 = Process(target = func_broker, args = (q_req,))
        p_broker2 = Process(target = func_broker, args = (q_req,))
        p_broker3 = Process(target = func_broker, args = (q_req,))
        p_broker4 = Process(target = func_broker, args = (q_req,))
        p_broker5 = Process(target = func_broker, args = (q_req,))
        p_broker6 = Process(target = func_broker, args = (q_req,))
        p_broker7 = Process(target = func_broker, args = (q_req,))
        p_broker8 = Process(target = func_broker, args = (q_req,))               
        """
        #//启动控制进程
        p_update = Process(target = update_trader_info_looped, args = (runtime,))
        p_control = Process(target = tradingObjects.positions_control_notNet_neutral_looped, args = (runtime,))
        #//运行master进程，负责获取行情数据并分流给四个trading子进程。
        is_first_loop = 1
        print_count = 0
        while True:
            print_count += 1
            #//update trader info
            #update_trader_info(runtime)
            #//update snapshots
            update_snapshots(runtime)
            #//进行仓位控制
            #tradingObjects.positions_control_notNet(runtime)
            #//如果是第一轮循环则启动进程
            if is_first_loop == 1:
                update_trader_info(runtime)
                tradingObjects.positions_control_notNet(runtime)
                p_update.start()
                p_control.start()
                """
                p_broker1.start()
                p_broker2.start()
                p_broker3.start()
                p_broker4.start()  
                p_broker5.start()
                p_broker6.start()
                p_broker7.start()
                p_broker8.start()                     
                """                                           
                p_A001.start()
                p_A002.start()
                p_B001.start()
                p_B002.start()
                is_first_loop = 0
            if print_count%10 == 0:
                print(runtime['snapshots_count'],runtime['trader_info_count'])
                print(runtime['loopCount_A001.PSE'],runtime['loopCount_A002.PSE'],
                    runtime['loopCount_B001.PSE'],runtime['loopCount_B002.PSE'])