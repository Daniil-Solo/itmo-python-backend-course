# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nauth.proto\x12\x04\x61uth\"/\n\x0cLoginRequest\x12\r\n\x05login\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"6\n\rLoginResponse\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x02\"#\n\rLogoutRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"\x10\n\x0eLogoutResponse\"!\n\x0bUserRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"\x1f\n\x0cUserResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\t2\xa7\x01\n\x0b\x41uthService\x12\x30\n\x05login\x12\x12.auth.LoginRequest\x1a\x13.auth.LoginResponse\x12\x33\n\x06logout\x12\x13.auth.LogoutRequest\x1a\x14.auth.LogoutResponse\x12\x31\n\x08get_user\x12\x11.auth.UserRequest\x1a\x12.auth.UserResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_LOGINREQUEST']._serialized_start=20
  _globals['_LOGINREQUEST']._serialized_end=67
  _globals['_LOGINRESPONSE']._serialized_start=69
  _globals['_LOGINRESPONSE']._serialized_end=123
  _globals['_LOGOUTREQUEST']._serialized_start=125
  _globals['_LOGOUTREQUEST']._serialized_end=160
  _globals['_LOGOUTRESPONSE']._serialized_start=162
  _globals['_LOGOUTRESPONSE']._serialized_end=178
  _globals['_USERREQUEST']._serialized_start=180
  _globals['_USERREQUEST']._serialized_end=213
  _globals['_USERRESPONSE']._serialized_start=215
  _globals['_USERRESPONSE']._serialized_end=246
  _globals['_AUTHSERVICE']._serialized_start=249
  _globals['_AUTHSERVICE']._serialized_end=416
# @@protoc_insertion_point(module_scope)
