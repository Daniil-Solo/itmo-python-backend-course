import grpc
from api_gateway.settings import settings
from protos.time_checking_pb2_grpc import CheckTimeServiceStub
from api_gateway.time_checking.service import TimeCheckingService


async def get_time_checking_service():
    """
    Зависимость для получения сервиса курсов по gRPC
    """
    async with grpc.aio.insecure_channel(settings.time_checking_grpc_server_address) as channel:
        stub = CheckTimeServiceStub(channel)
        course_service = TimeCheckingService(stub)
        yield course_service
