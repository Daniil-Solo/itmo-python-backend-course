# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protos.course_pb2 as course__pb2


class CourseServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_course_info = channel.unary_unary(
                '/course.CourseService/get_course_info',
                request_serializer=course__pb2.CourseRequest.SerializeToString,
                response_deserializer=course__pb2.CourseFullResponse.FromString,
                )
        self.get_courses = channel.unary_unary(
                '/course.CourseService/get_courses',
                request_serializer=course__pb2.CourseFilterRequest.SerializeToString,
                response_deserializer=course__pb2.CourseListResponse.FromString,
                )
        self.exists_course = channel.unary_unary(
                '/course.CourseService/exists_course',
                request_serializer=course__pb2.CourseRequest.SerializeToString,
                response_deserializer=course__pb2.CourseExistsResponse.FromString,
                )


class CourseServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_course_info(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_courses(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def exists_course(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CourseServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_course_info': grpc.unary_unary_rpc_method_handler(
                    servicer.get_course_info,
                    request_deserializer=course__pb2.CourseRequest.FromString,
                    response_serializer=course__pb2.CourseFullResponse.SerializeToString,
            ),
            'get_courses': grpc.unary_unary_rpc_method_handler(
                    servicer.get_courses,
                    request_deserializer=course__pb2.CourseFilterRequest.FromString,
                    response_serializer=course__pb2.CourseListResponse.SerializeToString,
            ),
            'exists_course': grpc.unary_unary_rpc_method_handler(
                    servicer.exists_course,
                    request_deserializer=course__pb2.CourseRequest.FromString,
                    response_serializer=course__pb2.CourseExistsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'course.CourseService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CourseService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_course_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/course.CourseService/get_course_info',
            course__pb2.CourseRequest.SerializeToString,
            course__pb2.CourseFullResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_courses(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/course.CourseService/get_courses',
            course__pb2.CourseFilterRequest.SerializeToString,
            course__pb2.CourseListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def exists_course(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/course.CourseService/exists_course',
            course__pb2.CourseRequest.SerializeToString,
            course__pb2.CourseExistsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
