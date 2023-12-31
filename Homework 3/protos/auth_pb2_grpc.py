# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protos.auth_pb2 as auth__pb2


class AuthServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.login = channel.unary_unary(
                '/auth.AuthService/login',
                request_serializer=auth__pb2.LoginRequest.SerializeToString,
                response_deserializer=auth__pb2.LoginResponse.FromString,
                )
        self.logout = channel.unary_unary(
                '/auth.AuthService/logout',
                request_serializer=auth__pb2.LogoutRequest.SerializeToString,
                response_deserializer=auth__pb2.LogoutResponse.FromString,
                )
        self.get_user = channel.unary_unary(
                '/auth.AuthService/get_user',
                request_serializer=auth__pb2.UserRequest.SerializeToString,
                response_deserializer=auth__pb2.UserResponse.FromString,
                )


class AuthServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def login(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def logout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_user(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'login': grpc.unary_unary_rpc_method_handler(
                    servicer.login,
                    request_deserializer=auth__pb2.LoginRequest.FromString,
                    response_serializer=auth__pb2.LoginResponse.SerializeToString,
            ),
            'logout': grpc.unary_unary_rpc_method_handler(
                    servicer.logout,
                    request_deserializer=auth__pb2.LogoutRequest.FromString,
                    response_serializer=auth__pb2.LogoutResponse.SerializeToString,
            ),
            'get_user': grpc.unary_unary_rpc_method_handler(
                    servicer.get_user,
                    request_deserializer=auth__pb2.UserRequest.FromString,
                    response_serializer=auth__pb2.UserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'auth.AuthService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AuthService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/auth.AuthService/login',
            auth__pb2.LoginRequest.SerializeToString,
            auth__pb2.LoginResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def logout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/auth.AuthService/logout',
            auth__pb2.LogoutRequest.SerializeToString,
            auth__pb2.LogoutResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_user(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/auth.AuthService/get_user',
            auth__pb2.UserRequest.SerializeToString,
            auth__pb2.UserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
