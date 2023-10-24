from api_gateway.time_checking.schemas import CourseList
from protos.time_checking_pb2_grpc import CheckTimeServiceStub
from protos.time_checking_pb2 import CheckTimeResponse, CheckTimeRequest, Course


class TimeCheckingService:  # pylint: disable=too-few-public-methods
    """Сервис для получения информации о пересечении курсов через gRPC"""
    def __init__(self, stub: CheckTimeServiceStub):
        self.stub = stub

    async def check(self, courses: CourseList) -> bool:
        """Проверяет отсутствие пересечений в занятия для переданных курсов"""
        response: CheckTimeResponse = await self.stub.check(
            CheckTimeRequest(courses=[Course(id=course_id) for course_id in courses.items])
        )
        return response.is_successful
