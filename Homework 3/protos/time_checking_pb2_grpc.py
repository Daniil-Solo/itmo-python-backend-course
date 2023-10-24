# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protos.time_checking_pb2 as time__checking__pb2


class CheckTimeServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.check = channel.unary_unary(
                '/time_checking.CheckTimeService/check',
                request_serializer=time__checking__pb2.CheckTimeRequest.SerializeToString,
                response_deserializer=time__checking__pb2.CheckTimeResponse.FromString,
                )


class CheckTimeServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def check(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CheckTimeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'check': grpc.unary_unary_rpc_method_handler(
                    servicer.check,
                    request_deserializer=time__checking__pb2.CheckTimeRequest.FromString,
                    response_serializer=time__checking__pb2.CheckTimeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'time_checking.CheckTimeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CheckTimeService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def check(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/time_checking.CheckTimeService/check',
            time__checking__pb2.CheckTimeRequest.SerializeToString,
            time__checking__pb2.CheckTimeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
