import asyncio
from grpc import aio
from protos.time_checking_pb2_grpc import add_CheckTimeServiceServicer_to_server
from time_checking.service.service import CheckTimeServicer
from time_checking.settings import settings


async def run_server():
    """Запускает сервер gRPC"""
    server = aio.server()
    add_CheckTimeServiceServicer_to_server(CheckTimeServicer(), server)
    server.add_insecure_port(settings.time_checking_grpc_server_address)
    await server.start()
    print("Server has started")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(run_server())
