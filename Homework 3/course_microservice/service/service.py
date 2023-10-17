from protos.course_pb2_grpc import CourseServiceServicer
from protos.course_pb2 import (
    CourseFullResponse, CourseListResponse, CourseExistsResponse, CourseRequest, CourseFilterRequest
)
from course_microservice.service.repository import CourseRepositoryContextManager


class CourseServicer(CourseServiceServicer):
    async def get_course_info(self, request: CourseRequest, context) -> CourseFullResponse:
        async with CourseRepositoryContextManager() as course_repo:
            course = await course_repo.one(request.course_id)
            if course is None:
                return CourseFullResponse(id=None)
        return course.to_grpc_response()

    async def get_courses(self, request: CourseFilterRequest, context) -> CourseListResponse:
        async with CourseRepositoryContextManager() as course_repo:
            courses = await course_repo.list()
        filtered_courses = courses
        if request.implementer:
            filtered_courses = filter(lambda c: c.implementer == request.implementer, filtered_courses)
        if request.role:
            filtered_courses = filter(lambda c: request.role in c.roles, filtered_courses)
        if request.search:
            filtered_courses = filter(lambda c: request.search.lower() in c.name.lower(), filtered_courses)
        return CourseListResponse(
            courses=[course.to_grpc_response() for course in filtered_courses]
        )

    async def exists_course(self, request: CourseRequest, context) -> CourseExistsResponse:
        async with CourseRepositoryContextManager() as course_repo:
            is_existed = await course_repo.exists(request.course_id)
        return CourseExistsResponse(exists=is_existed)
