# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0c\x63ommon.proto\"\x07\n\x05\x45mpty\"x\n\x0bRpcResponse\x12\"\n\x0crequest_type\x18\x01 \x01(\x0e\x32\x0c.RequestType\x12\x11\n\ttrader_id\x18\x02 \x01(\x05\x12\x10\n\x08order_id\x18\x03 \x01(\x03\x12 \n\x0bresult_code\x18\x04 \x01(\x0e\x32\x0b.ResultCode\"d\n\x0eInstrumentInfo\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\ninit_price\x18\x03 \x01(\x01\x12\x0c\n\x04tick\x18\x04 \x01(\x01\x12\x12\n\nlast_price\x18\x05 \x01(\x01\":\n\x12InstrumentInfoList\x12$\n\x0binstruments\x18\x01 \x03(\x0b\x32\x0f.InstrumentInfo\"A\n\x0bQuoteRecord\x12\r\n\x05price\x18\x01 \x01(\x01\x12\x0e\n\x06volume\x18\x02 \x01(\x05\x12\x13\n\x0border_count\x18\x03 \x01(\x05\"?\n\x0bTradeRecord\x12\x11\n\ttimestamp\x18\x01 \x01(\x01\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x0e\n\x06volume\x18\x03 \x01(\x05*\x18\n\x04Side\x12\x07\n\x03\x42ID\x10\x00\x12\x07\n\x03\x41SK\x10\x01*#\n\x0cPositionType\x12\x08\n\x04LONG\x10\x00\x12\t\n\x05SHORT\x10\x01*e\n\x0bRequestType\x12\r\n\tNEW_ORDER\x10\x00\x12\x10\n\x0c\x43\x41NCEL_ORDER\x10\x01\x12\x10\n\x0cMODIFY_ORDER\x10\x02\x12\x14\n\x10INCREMENTAL_INFO\x10\x03\x12\r\n\tFULL_INFO\x10\x04*\xe4\x03\n\nResultCode\x12\x06\n\x02OK\x10\x00\x12\x11\n\rUNKNOWN_ERROR\x10\x63\x12\x17\n\x13SERVICE_UNAVAILABLE\x10\x64\x12\x15\n\x11REGISTER_DISABLED\x10x\x12\x14\n\x0fINVALID_REQUEST\x10\xc8\x01\x12\x11\n\x0cUNAUTHORIZED\x10\xc9\x01\x12\x11\n\x0cUNSUBSCRIBED\x10\xca\x01\x12\x16\n\x11TOO_MANY_REQUESTS\x10\xd2\x01\x12\x14\n\x0fTOO_MANY_ORDERS\x10\xd3\x01\x12\x12\n\rINVALID_ORDER\x10\xdc\x01\x12\x16\n\x11INVALID_BROKER_ID\x10\xdd\x01\x12\x15\n\x10INVALID_ORDER_ID\x10\xde\x01\x12\x16\n\x11INVALID_TRADER_ID\x10\xdf\x01\x12\x18\n\x13INVALID_TRADER_NAME\x10\xe0\x01\x12\x13\n\x0eINVALID_SYMBOL\x10\xf1\x01\x12\x12\n\rINVALID_PRICE\x10\xf2\x01\x12\x13\n\x0eINVALID_VOLUME\x10\xf3\x01\x12\x11\n\x0cINVALID_SIDE\x10\xf4\x01\x12\x15\n\x10INVALID_POSITION\x10\xf5\x01\x12\x18\n\x13INSUFFICIENT_ASSETS\x10\x84\x02\x12\x15\n\x10\x41\x43\x43OUNT_DISABLED\x10\x8e\x02\x12\x13\n\x0eON_MARGIN_CALL\x10\x8f\x02*\x82\x01\n\nOrderState\x12\x11\n\rORDER_INITIAL\x10\x00\x12\x12\n\x0eORDER_ACCEPTED\x10\x01\x12\x10\n\x0cORDER_TRADED\x10\x02\x12\x12\n\x0eORDER_FINISHED\x10\x03\x12\x13\n\x0fORDER_CANCELLED\x10\x04\x12\x12\n\x0eORDER_REJECTED\x10\x05\x62\x06proto3')
)

_SIDE = _descriptor.EnumDescriptor(
  name='Side',
  full_name='Side',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BID', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASK', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=441,
  serialized_end=465,
)
_sym_db.RegisterEnumDescriptor(_SIDE)

Side = enum_type_wrapper.EnumTypeWrapper(_SIDE)
_POSITIONTYPE = _descriptor.EnumDescriptor(
  name='PositionType',
  full_name='PositionType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LONG', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHORT', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=467,
  serialized_end=502,
)
_sym_db.RegisterEnumDescriptor(_POSITIONTYPE)

PositionType = enum_type_wrapper.EnumTypeWrapper(_POSITIONTYPE)
_REQUESTTYPE = _descriptor.EnumDescriptor(
  name='RequestType',
  full_name='RequestType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NEW_ORDER', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANCEL_ORDER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MODIFY_ORDER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INCREMENTAL_INFO', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FULL_INFO', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=504,
  serialized_end=605,
)
_sym_db.RegisterEnumDescriptor(_REQUESTTYPE)

RequestType = enum_type_wrapper.EnumTypeWrapper(_REQUESTTYPE)
_RESULTCODE = _descriptor.EnumDescriptor(
  name='ResultCode',
  full_name='ResultCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_ERROR', index=1, number=99,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERVICE_UNAVAILABLE', index=2, number=100,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REGISTER_DISABLED', index=3, number=120,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_REQUEST', index=4, number=200,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNAUTHORIZED', index=5, number=201,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNSUBSCRIBED', index=6, number=202,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_REQUESTS', index=7, number=210,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_ORDERS', index=8, number=211,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_ORDER', index=9, number=220,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_BROKER_ID', index=10, number=221,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_ORDER_ID', index=11, number=222,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_TRADER_ID', index=12, number=223,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_TRADER_NAME', index=13, number=224,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_SYMBOL', index=14, number=241,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_PRICE', index=15, number=242,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_VOLUME', index=16, number=243,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_SIDE', index=17, number=244,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_POSITION', index=18, number=245,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INSUFFICIENT_ASSETS', index=19, number=260,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACCOUNT_DISABLED', index=20, number=270,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ON_MARGIN_CALL', index=21, number=271,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=608,
  serialized_end=1092,
)
_sym_db.RegisterEnumDescriptor(_RESULTCODE)

ResultCode = enum_type_wrapper.EnumTypeWrapper(_RESULTCODE)
_ORDERSTATE = _descriptor.EnumDescriptor(
  name='OrderState',
  full_name='OrderState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ORDER_INITIAL', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ORDER_ACCEPTED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ORDER_TRADED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ORDER_FINISHED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ORDER_CANCELLED', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ORDER_REJECTED', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1095,
  serialized_end=1225,
)
_sym_db.RegisterEnumDescriptor(_ORDERSTATE)

OrderState = enum_type_wrapper.EnumTypeWrapper(_ORDERSTATE)
BID = 0
ASK = 1
LONG = 0
SHORT = 1
NEW_ORDER = 0
CANCEL_ORDER = 1
MODIFY_ORDER = 2
INCREMENTAL_INFO = 3
FULL_INFO = 4
OK = 0
UNKNOWN_ERROR = 99
SERVICE_UNAVAILABLE = 100
REGISTER_DISABLED = 120
INVALID_REQUEST = 200
UNAUTHORIZED = 201
UNSUBSCRIBED = 202
TOO_MANY_REQUESTS = 210
TOO_MANY_ORDERS = 211
INVALID_ORDER = 220
INVALID_BROKER_ID = 221
INVALID_ORDER_ID = 222
INVALID_TRADER_ID = 223
INVALID_TRADER_NAME = 224
INVALID_SYMBOL = 241
INVALID_PRICE = 242
INVALID_VOLUME = 243
INVALID_SIDE = 244
INVALID_POSITION = 245
INSUFFICIENT_ASSETS = 260
ACCOUNT_DISABLED = 270
ON_MARGIN_CALL = 271
ORDER_INITIAL = 0
ORDER_ACCEPTED = 1
ORDER_TRADED = 2
ORDER_FINISHED = 3
ORDER_CANCELLED = 4
ORDER_REJECTED = 5



_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=16,
  serialized_end=23,
)


_RPCRESPONSE = _descriptor.Descriptor(
  name='RpcResponse',
  full_name='RpcResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_type', full_name='RpcResponse.request_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trader_id', full_name='RpcResponse.trader_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order_id', full_name='RpcResponse.order_id', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result_code', full_name='RpcResponse.result_code', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=145,
)


_INSTRUMENTINFO = _descriptor.Descriptor(
  name='InstrumentInfo',
  full_name='InstrumentInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='symbol', full_name='InstrumentInfo.symbol', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='InstrumentInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='init_price', full_name='InstrumentInfo.init_price', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tick', full_name='InstrumentInfo.tick', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='last_price', full_name='InstrumentInfo.last_price', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=247,
)


_INSTRUMENTINFOLIST = _descriptor.Descriptor(
  name='InstrumentInfoList',
  full_name='InstrumentInfoList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instruments', full_name='InstrumentInfoList.instruments', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=249,
  serialized_end=307,
)


_QUOTERECORD = _descriptor.Descriptor(
  name='QuoteRecord',
  full_name='QuoteRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='price', full_name='QuoteRecord.price', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='volume', full_name='QuoteRecord.volume', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order_count', full_name='QuoteRecord.order_count', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=309,
  serialized_end=374,
)


_TRADERECORD = _descriptor.Descriptor(
  name='TradeRecord',
  full_name='TradeRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='TradeRecord.timestamp', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='price', full_name='TradeRecord.price', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='volume', full_name='TradeRecord.volume', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=376,
  serialized_end=439,
)

_RPCRESPONSE.fields_by_name['request_type'].enum_type = _REQUESTTYPE
_RPCRESPONSE.fields_by_name['result_code'].enum_type = _RESULTCODE
_INSTRUMENTINFOLIST.fields_by_name['instruments'].message_type = _INSTRUMENTINFO
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['RpcResponse'] = _RPCRESPONSE
DESCRIPTOR.message_types_by_name['InstrumentInfo'] = _INSTRUMENTINFO
DESCRIPTOR.message_types_by_name['InstrumentInfoList'] = _INSTRUMENTINFOLIST
DESCRIPTOR.message_types_by_name['QuoteRecord'] = _QUOTERECORD
DESCRIPTOR.message_types_by_name['TradeRecord'] = _TRADERECORD
DESCRIPTOR.enum_types_by_name['Side'] = _SIDE
DESCRIPTOR.enum_types_by_name['PositionType'] = _POSITIONTYPE
DESCRIPTOR.enum_types_by_name['RequestType'] = _REQUESTTYPE
DESCRIPTOR.enum_types_by_name['ResultCode'] = _RESULTCODE
DESCRIPTOR.enum_types_by_name['OrderState'] = _ORDERSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  ))
_sym_db.RegisterMessage(Empty)

RpcResponse = _reflection.GeneratedProtocolMessageType('RpcResponse', (_message.Message,), dict(
  DESCRIPTOR = _RPCRESPONSE,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:RpcResponse)
  ))
_sym_db.RegisterMessage(RpcResponse)

InstrumentInfo = _reflection.GeneratedProtocolMessageType('InstrumentInfo', (_message.Message,), dict(
  DESCRIPTOR = _INSTRUMENTINFO,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:InstrumentInfo)
  ))
_sym_db.RegisterMessage(InstrumentInfo)

InstrumentInfoList = _reflection.GeneratedProtocolMessageType('InstrumentInfoList', (_message.Message,), dict(
  DESCRIPTOR = _INSTRUMENTINFOLIST,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:InstrumentInfoList)
  ))
_sym_db.RegisterMessage(InstrumentInfoList)

QuoteRecord = _reflection.GeneratedProtocolMessageType('QuoteRecord', (_message.Message,), dict(
  DESCRIPTOR = _QUOTERECORD,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:QuoteRecord)
  ))
_sym_db.RegisterMessage(QuoteRecord)

TradeRecord = _reflection.GeneratedProtocolMessageType('TradeRecord', (_message.Message,), dict(
  DESCRIPTOR = _TRADERECORD,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:TradeRecord)
  ))
_sym_db.RegisterMessage(TradeRecord)


# @@protoc_insertion_point(module_scope)
