"""
Filename: engine.py
"""

import proto_wrapper as api

import broker_pb2
import grpc
import common_pb2
import broker_pb2_grpc

from multiprocessing import Process,Queue
import os
import numpy as np
from time import ctime, sleep,time_ns,time

ID = 33
PIN = 'jY0RyHyK9'
CHANNEL_BROKER = grpc.insecure_channel('113.208.112.25:57500') 
CHANNEL_DATA = grpc.insecure_channel('113.208.112.25:57600')

time_now = time_ns()

broker_stub = broker_pb2_grpc.BrokerStub(CHANNEL_BROKER)
data_stub = broker_pb2_grpc.MarketDataStub(CHANNEL_DATA)
#//创建客户端

data_stream = data_stub.subscribe(broker_pb2.TraderRequest(trader_id = ID, trader_pin = PIN))

api.set_stub(broker = broker_stub, data = data_stub)
api.set_stream(data_stream)

print("Set up stub used %.9f"%(time_ns() - time_now))
time_now = time_ns()

#//测试行情订阅
for i in range(1000):
    snapshot_new = data_stream.next()

print('Subscribe one snapshot used %.9f'%((time_ns() - time_now)/1000))
time_now = time_ns()

#//下单
for i in range(1000):
    broker_stub.new_order(api.TraderRequest_new_order('A002',0,0,1,100))

print('Place one new order used %.9f'%((time_ns() - time_now)/1000))
time_now = time_ns()

#//获取用户信息
for i in range(1000):
    info = broker_stub.get_trader(api.TraderRequest_get_trader_full())

print('Get my info used %.9f'%((time_ns()-time_now)/1000))