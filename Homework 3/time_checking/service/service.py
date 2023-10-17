import grpc
from typing import Iterable
from protos.course_pb2 import CourseFullResponse, CourseRequest, CourseExistsResponse
from protos.course_pb2_grpc import CourseServiceStub
from protos.time_checking_pb2_grpc import CheckTimeServiceServicer
from protos.time_checking_pb2 import CheckTimeRequest, CheckTimeResponse, Course
from time_checking.settings import settings


class CheckTimeServicer(CheckTimeServiceServicer):
    async def check(self, request: CheckTimeRequest, context) -> CheckTimeResponse:
        courses = self.get_courses(request.courses)
        is_successful = self.check_time_for_lessons(courses)
        return CheckTimeResponse(is_successful=is_successful)

    @staticmethod
    def get_courses(course_list: Iterable[Course]) -> list[CourseFullResponse]:
        """
        Возвращает курсы с подробной информацией о расписании
        Изначально был сделан асинхронный вариант, но сервер при таком варианте вылетал без ошибки
        :param course_list: курсы с информацией об идентификаторе курса
        :return: курсы с расписанием занятий
        """
        courses = []
        with grpc.insecure_channel(settings.course_grpc_server_address) as channel:
            stub = CourseServiceStub(channel)
            for course_id in [course.id for course in course_list]:
                course_exists: CourseExistsResponse = stub.exists_course(CourseRequest(course_id=course_id))
                if course_exists.exists:
                    course = stub.get_course_info(CourseRequest(course_id=course_id))
                    courses.append(course)
        return courses

    @staticmethod
    def check_time_for_lessons(courses: Iterable[CourseFullResponse]) -> bool:
        """
        Проверяет, есть ли занятия в курсах плана, которые будут пересекаться во времени
        Считается, что одно занятие начинается строго в определенное время и не может продолжаться больше
        2 пар (~3 часов)
        :param courses: курсы
        :return: удастся ли изучить все курсы
        """
        lessons = []
        for course in courses:
            for lesson in course.lessons:
                start_time, finish_time = lesson.string_time_interval.split(" - ")
                day = lesson.string_day
                lessons.append((day, start_time))
                lessons.append((day, finish_time))
        return len(lessons) == len(set(lessons))
