import grpc
from protos.auth_pb2_grpc import AuthServiceStub
from api_gateway.settings import settings
from api_gateway.auth.service import AuthService


async def get_auth_service():
    """
    Зависимость для получения сервиса аутентификации по gRPC
    """
    async with grpc.aio.insecure_channel(settings.auth_grpc_server_address) as channel:
        stub = AuthServiceStub(channel)
        auth_service = AuthService(stub)
        yield auth_service
