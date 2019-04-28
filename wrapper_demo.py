import grpc
import broker_pb2
import broker_pb2_grpc
import proto_wrapper
from time import sleep
from time import ctime

api = proto_wrapper
"""
Const
"""

ID = 33
PIN = 'jY0RyHyK9'

"""
创建客户端
"""

#Create channel
broker_channel = grpc.insecure_channel('113.208.112.25:57503')
data_channel = grpc.insecure_channel('113.208.112.25:57600')
#create stub
broker_stub = broker_pb2_grpc.BrokerStub(broker_channel)
md_stub = broker_pb2_grpc.MarketDataStub(data_channel)

api.set_stub(broker_stub, md_stub)
"""
Demo: 下单
"""
TraderRequest_new_order = broker_pb2.TraderRequest(trader_id = ID, trader_pin = PIN, request_type=0,
                                                   order_id = 0, side = 0, symbol = 'A000.PSE', volume = 1,
                                                   is_market = True, pos_type = 1)
TraderRequest_new_order_test=  proto_wrapper.TraderRequest_new_order("A000.PSE",side=0,pos_type=0,volume=1,is_market=False,price=90)                                    
response_new_order = broker_stub.new_order(TraderRequest_new_order_test)
print(response_new_order)
print ("##########################################")



"""
Demo: 撤单
"""
TraderRequest_cancel_order = proto_wrapper.TraderRequest_cancel_order(order_id = tuple(response_new_order.orders.orders.keys())[0])
response_cancel_order = broker_stub.cancel_order(TraderRequest_cancel_order)
print (response_cancel_order)
print ("##########################################")


"""
获取增量账户信息和完整的账户信息
"""

TraderRequest_get_trader_incremental = proto_wrapper.TraderRequest_get_trader_inc()
response_get_trader_incremental = broker_stub.get_trader(TraderRequest_get_trader_incremental)
print(response_get_trader_incremental)
print ("##########################################")
TraderRequest_get_trader_full = proto_wrapper.TraderRequest_get_trader_full()
response_get_trader_full = broker_stub.get_trader(TraderRequest_get_trader_full)
print(response_get_trader_full)
print ("##########################################")

                                                
#获取data流对象
market_data_stream = md_stub.subscribe(broker_pb2.TraderRequest(trader_id=33, trader_pin='jY0RyHyK9'))
if market_data_stream.is_active:
    while True:
        market_data_snapshot = market_data_stream.next()
        for insturment_data in market_data_snapshot.instruments:
            print("[%s] GET instrument %s at timestamp %s"%(ctime(),insturment_data.symbol,insturment_data.timestamp))
        sleep(1)
else:
    print("Error: Bad gateway")
#, Side side =BID, string symbol ='A001.PSE', int32 volume =10,PositionType pos_type ='LONG'


"""
#Market data stream 的结构
创建行情数据流对象（以下简称inflow）后，可以调用inflow.is_active检查57600端口的该方法是否在执行服务。如果active为True，
则可以调用inflow.next()获取最新的行情截面快照。
快照的结构为树形：

snapshot
{
    6个instruments(六个产品，A00到B02)生成六个节点
    {
        每个产品的可用fields
        {
            跟市场信息相关的有如下：
            
            symbol:该产品的名字
            timestamp:该数据结构体的截面的时间
            last_price:上一笔成交的价格
            bid_volume:当前挂单的买单总量（注意不是订单数，因为一个订单可以挂任何买量）
            ask_volume:当前挂单的卖单总量
            bid_order_count:买单挂单订单数
            ask_order_count:卖单挂单订单数
            bid_depth:买单深度，应该是指所有买单所挂的价格水平的总数，我不确定
            ask_depth:卖单深度，同上
            last_trades:一个列表，里面有最近成交的一些成交价格和成交量的信息，且按时间排好序了
            bid_levels:一个列表，里面有所有10档买方竞价
            ask_levels:一个列表，里面有所有10档卖方降价
        }
    }
}
"""