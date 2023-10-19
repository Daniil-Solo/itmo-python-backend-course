from typing import Optional
from protos.course_pb2_grpc import CourseServiceStub
from protos.course_pb2 import CourseFilterRequest, CourseRequest, CourseListResponse, CourseFullResponse
from api_gateway.courses.schemas import CourseShort, CourseFull, Lesson
from api_gateway.courses.exceptions import CourseDoesntExist


class CourseService:
    """Сервис для курсов через gRPC"""
    def __init__(self, stub: CourseServiceStub):
        self.stub = stub

    async def get_courses(
            self,
            implementer: Optional[str] = None,
            role: Optional[str] = None,
            search: Optional[str] = None) -> list[CourseShort]:
        """Возвращает курсы по переданным фильтрам"""
        response: CourseListResponse = await self.stub.get_courses(
            CourseFilterRequest(implementer=implementer, role=role, search=search)
        )
        return [
            CourseShort(id=course.id, name=course.name, is_prerecorded_course=course.is_prerecorded_course)
            for course in response.courses
        ]

    async def get_course_info(self, course_id: int) -> CourseFull:
        """Возвращает подробную информацию о курсе или вызывает ошибку"""
        response: CourseFullResponse = await self.stub.get_course_info(CourseRequest(course_id=course_id))
        if response.id == 0:
            raise CourseDoesntExist
        return CourseFull(
            id=response.id,
            name=response.name,
            description=response.description,
            is_prerecorded_course=response.is_prerecorded_course,
            implementer=response.implementer,
            roles=list(response.roles),
            lessons=[
                Lesson(
                    number=lesson.number, day_of_week=lesson.day_of_week, string_day=lesson.string_day,
                    string_time_interval=lesson.string_time_interval
                )
                for lesson in response.lessons
            ]
        )
