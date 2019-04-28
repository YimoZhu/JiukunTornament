#//Filename: proto_warpper.py
#封装broker proto对象

import grpc
import broker_pb2_grpc
import broker_pb2

#Configuration
ID = 24
PIN = "jY0RyHyK9"
REQUEST_TYPE = {
    "NEW_ORDER" : 0,
    "CANCEL_ORDER" : 1,
    "MODIFY_ORDER" : 2,  
    "INCREMENTAL_INFO" : 3,
    "FULL_INFO" : 4,    
}
POS_TYPE_LONG = 0
POS_TYPE_SHORT = 1

def TraderRequest(*args,**kw):
    return broker_pb2.TraderRequest(trader_id = ID, trader_pin = PIN, *args, **kw)

def TraderRequest_new_order(symbol,side,pos_type,volume,price=None,is_market=False,*args,**kw):
    return broker_pb2.TraderRequest(trader_id = ID, trader_pin = PIN, request_type = 0,
                                    side = side, symbol = symbol, pos_type = pos_type, volume = volume,
                                    price = price, is_market = is_market, *args, **kw)

def TraderRequest_cancel_order(order_id,*args,**kw):
    return broker_pb2.TraderRequest(trader_id = ID, trader_pin = PIN, request_type = 1,
                                    order_id = order_id, *args, **kw)

def TraderRequest_get_trader_full():
    return broker_pb2.TraderRequest(trader_id = ID, trader_pin = PIN, request_type = 4)

def TraderRequest_get_trader_inc():
    return broker_pb2.TraderRequest(trader_id = ID, trader_pin = PIN, request_type = 3)

def set_stub(broker, data):
    global broker_stub
    global data_stub
    broker_stub = broker
    data_stub = data

def set_stream(stream):
    global data_stream 
    data_stream = stream

def cancel_all():
    global broker_stub
    for order in broker_stub.get_trader(TraderRequest_get_trader_full()).orders.orders.keys():
        broker_stub.cancel_order(TraderRequest_cancel_order(order))

def close_all_at_market(symbol = 'ALL'):
    global broker_stub
    pos_info = broker_stub.get_trader(TraderRequest_get_trader_full()).positions
    if symbol == "ALL":
        for i,j in pos_info.long_positions.items():
            broker_stub.new_order(TraderRequest_new_order(i,1,0,j.volume,is_market=True))
        for i,j in pos_info.short_positions.items():
            broker_stub.new_order(TraderRequest_new_order(i,0,1,j.volume,is_market=True))

def get_trader_full():
    return broker_stub.get_trader(TraderRequest_get_trader_full())

def get_trader_inc():
    return broker_stub.get_trader(TraderRequest_get_trader_inc())
    
def get_trader_info(me_only=True):
    if me_only:
        return broker_stub.get_traders_info(TraderRequest()).traders[ID-1]
    else:
        return broker_stub.get_traders_info(TraderRequest())