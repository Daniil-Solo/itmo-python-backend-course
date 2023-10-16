import os
import asyncio
from grpc import aio
from protos.course_pb2_grpc import add_CourseServiceServicer_to_server
from course_microservice.service.service import CourseServicer
from course_microservice.settings import settings
from course_microservice.database.data import migrate, create_data


async def run_server():
    if not os.path.exists(settings.db_filepath):
        await migrate()
        await create_data()
        print("Migrations have been applied")
    server = aio.server()
    add_CourseServiceServicer_to_server(CourseServicer(), server)
    server.add_insecure_port(settings.course_grpc_server_address)
    await server.start()
    print("Server has started")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(run_server())
