from copy import deepcopy
import numpy as np

class null_position(object):
    def __init__(self):
        self.volume = 0
        self.locked_volume = 0

class order_info(object):
    def __init__(self, trader_info):
        trader_info = deepcopy(trader_info)
        self.info = {'A001.PSE':{},'B001.PSE':{},'A002.PSE':{},'B002.PSE':{}}
        for orderID, order in trader_info.orders.orders.items():
            self.info[order.symbol][orderID] = order

class positions_info(object):
    def __init__(self, trader_info):
        trader_info = deepcopy(trader_info)
        self.info = {'A001.PSE':{'long_positions':null_position(), 'short_positions':null_position()},
                     'B001.PSE':{'long_positions':null_position(), 'short_positions':null_position()},
                     'A002.PSE':{'long_positions':null_position(), 'short_positions':null_position()},
                     'B002.PSE':{'long_positions':null_position(), 'short_positions':null_position()}} 
        for symbol, pos in trader_info.positions.long_positions.items():
            self.info[symbol]['long_positions'] = pos
        for symbol, pos in trader_info.positions.short_positions.items():
            self.info[symbol]['short_positions'] = pos

class snapshots(object):
    def __init__(self, instruments):
        instruments = deepcopy(instruments)
        for instrument in instruments:
            setattr(self, instrument.symbol, instrument)
            setattr(self, instrument.symbol + '_digested', False)
        self.timestamp = getattr(self, 'A000.PSE').timestamp

def positions_control_notNet(runtime):
    for symbol in ['A001.PSE','B001.PSE','A002.PSE','B002.PSE']:
        #//开平仓的控制，当最小的头寸小于100的时候就开仓，以防止资产不足。
        positions_info = runtime['positions_info'].info[symbol]
        currLongPos = positions_info['long_positions'].volume + positions_info['long_positions'].locked_volume
        currShortPos = positions_info['short_positions'].volume + positions_info['short_positions'].locked_volume
        minPos = min(currLongPos,currShortPos)
        if minPos < 100:
            runtime['isOpen_'+symbol] = True
        else: 
            runtime['isOpen_'+symbol] = False
        #//净头寸控制，防止单边累计过多
        if currLongPos > currShortPos:
            runtime['net_'+symbol] = 1
        elif currLongPos < currShortPos:
            runtime['net_'+symbol] = -1
        else:
            runtime['net_'+symbol] = 0

def positions_control_notNet_looped(runtime):
    while True:
        for symbol in ['A001.PSE','B001.PSE','A002.PSE','B002.PSE']:
            #//开平仓的控制，当最小的头寸小于100的时候就开仓，以防止资产不足。
            positions_info = runtime['positions_info'].info[symbol]
            currLongPos = positions_info['long_positions'].volume + positions_info['long_positions'].locked_volume
            currShortPos = positions_info['short_positions'].volume + positions_info['short_positions'].locked_volume
            minPos = min(currLongPos,currShortPos)
            if minPos < 100:
                runtime['isOpen_'+symbol] = True
            else: 
                runtime['isOpen_'+symbol] = False
            #//净头寸控制，防止单边累计过多
            currNetPos = currLongPos - currShortPos
            if currNetPos > runtime['targetNetPos_'+symbol]:
                runtime['net_'+symbol] = 1
            elif currNetPos < runtime['targetNetPos_'+symbol]:
                runtime['net_'+symbol] = -1
            else:
                runtime['net_'+symbol] = 0


class snapshot_arbitrage_container(object):
    STATUS_ACTIVATED = 200
    STATUS_NONACTIVATED = 630
    def __init__(self,length):
        self.maxLen = length
        self.A002_arr = np.array([np.nan]*length)
        self.B002_arr = np.array([np.nan]*length)
        self.A002_arr_len = 0
        self.B002_arr_len = 0

        self.mean_A002 = self.A002_arr.mean()
        self.mean_B002 = self.B002_arr.mean()

        self.currTS = 0
        self.status = self.STATUS_NONACTIVATED

    def update(self,snapshot):
        #//更新价格序列
        if self.A002_arr_len < self.maxLen:
            self.A002_arr[self.A002_arr_len] = getattr(snapshot,'A000.PSE').last_price
            self.A002_arr_len += 1
        else:
            self.A002_arr[-1] = getattr(snapshot, 'A000.PSE').last_price
            self.A002_arr[:-1] = self.A002_arr[1:]
        if self.B002_arr_len < self.maxLen:
            self.B002_arr[self.B002_arr_len] = getattr(snapshot,'B000.PSE').last_price
            self.B002_arr_len += 1
        else:
            self.B002_arr[-1] = getattr(snapshot, 'B000.PSE').last_price
            self.B002_arr[:-1] = self.B002_arr[1:]
        #//更新均价
        self.mean_A002 = self.A002_arr.mean()
        self.mean_B002 = self.B002_arr.mean()
        #//更新时间戳
        self.currTS = snapshot.timestamp
        self.handle_timestamp()

    def handle_timestamp(self):
        #//处理时间戳
        moded_ts = self.currTS%900
        if moded_ts < 820:
            self.status = self.STATUS_NONACTIVATED
        else:
            if (self.A002_arr_len == self.maxLen)&(self.B002_arr_len == self.maxLen):
                #//如果数据也充足
                self.status = self.STATUS_ACTIVATED

    def get_settle_A002(self):
        return (self.mean_A002)**2/100
    
    def get_settle_B002(self):
        return self.mean_B002**0.5*10

    def get_targetNetPos_A002(self):
        last_price = self.A002_arr[-1]
        if self.get_settle_A002() > last_price:
            return 300
        elif self.get_settle_A002() < last_price:
            return -300
    
    def get_targetNetPos_B002(self):
        last_price = self.B002_arr[-1]
        if self.get_settle_B002() > last_price:
            return 300
        elif self.get_settle_B002() < last_price:
            return -300

def arbitrage(runtime):
    """
    套利进程，进行A002和B002合约的套利
    """
    container = snapshot_arbitrage_container(60)
    while True:
        if runtime['isDigested_arbitrage'] == 0:
            snapshot = runtime['snapshots']
            runtime['isDigested_arbitrage'] = 1
            container.update(snapshot)
            #//更新价格序列
            if container.status == container.STATUS_ACTIVATED:
                #//如果临近结算期，套利机制被激活，则修改仓位控制目标，使仓位向结算套利方向运动。
                runtime['targetNetPos_A002.PSE'] = container.get_targetNetPos_A002()
                runtime['targetNetPos_B002.PSE'] = container.get_targetNetPos_B002()
            else:
                runtime['targetNetPos_A002.PSE'] = 0
                runtime['targetNetPos_B002.PSE'] = 0
        else:
            pass
            
def positions_control_notNet_neutral_looped(runtime):
    while True:
        for symbol in ['A001.PSE','B001.PSE','A002.PSE','B002.PSE']:
            #//开平仓的控制，当最小的头寸小于100的时候就开仓，以防止资产不足。
            positions_info = runtime['positions_info'].info[symbol]
            currLongPos = positions_info['long_positions'].volume + positions_info['long_positions'].locked_volume
            currShortPos = positions_info['short_positions'].volume + positions_info['short_positions'].locked_volume
            minPos = min(currLongPos,currShortPos)
            if minPos < 100:
                runtime['isOpen_'+symbol] = True
            else: 
                runtime['isOpen_'+symbol] = False
            #//净头寸控制，防止单边累计过多
            runtime['net_'+symbol] = 0
            """
            if currLongPos > currShortPos:
                runtime['net_'+symbol] = 1
            elif currLongPos < currShortPos:
                runtime['net_'+symbol] = -1
            else:
                runtime['net_'+symbol] = 0
            """
        


class price_arr(object):
    mid_price = np.array([[-0.07,-0.05],
                          [ 0.05, 0.07]])
    mid_volume = np.array([[10,10],
                           [10,10]])