# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: time_checking.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13time_checking.proto\x12\rtime_checking\"\x14\n\x06\x43ourse\x12\n\n\x02id\x18\x01 \x01(\x05\":\n\x10\x43heckTimeRequest\x12&\n\x07\x63ourses\x18\x01 \x03(\x0b\x32\x15.time_checking.Course\"*\n\x11\x43heckTimeResponse\x12\x15\n\ris_successful\x18\x01 \x01(\x08\x32^\n\x10\x43heckTimeService\x12J\n\x05\x63heck\x12\x1f.time_checking.CheckTimeRequest\x1a .time_checking.CheckTimeResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'time_checking_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_COURSE']._serialized_start=38
  _globals['_COURSE']._serialized_end=58
  _globals['_CHECKTIMEREQUEST']._serialized_start=60
  _globals['_CHECKTIMEREQUEST']._serialized_end=118
  _globals['_CHECKTIMERESPONSE']._serialized_start=120
  _globals['_CHECKTIMERESPONSE']._serialized_end=162
  _globals['_CHECKTIMESERVICE']._serialized_start=164
  _globals['_CHECKTIMESERVICE']._serialized_end=258
# @@protoc_insertion_point(module_scope)