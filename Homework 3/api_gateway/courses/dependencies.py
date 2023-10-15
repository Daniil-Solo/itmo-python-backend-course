import grpc
from api_gateway.settings import settings
from protos.course_pb2_grpc import CourseServiceStub
from api_gateway.courses.service import CourseService


async def get_course_service():
    """
    Зависимость для получения сервиса курсов по gRPC
    """
    async with grpc.aio.insecure_channel(settings.course_grpc_server_address) as channel:
        stub = CourseServiceStub(channel)
        course_service = CourseService(stub)
        yield course_service
