import os
import asyncio
from grpc import aio
from protos.auth_pb2_grpc import add_AuthServiceServicer_to_server
from auth_microservice.service.service import AuthServicer
from auth_microservice.settings import settings
from auth_microservice.database.data import migrate, create_data


async def run_server():
    if not os.path.exists(settings.db_filepath):
        await migrate()
        await create_data()
        print("Migrations have been applied")
    server = aio.server()
    add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port(settings.auth_grpc_server_address)
    await server.start()
    print("Server has started")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(run_server())
