from datetime import datetime
from dataclasses import dataclass
from course_microservice.database.models import Course as CourseModel
from course_microservice.service.utils import format_lesson_time
from protos.course_pb2 import Lesson as LessonResponse, CourseShort as CourseShortResponse, CourseFullResponse


@dataclass
class Lesson:
    """
    Класс, описывающий занятие курса
    """
    number: int
    day_of_week: str
    string_day: str
    string_time_interval: str

    @staticmethod
    def from_data(number: int, start_time: datetime, finish_time: datetime):
        """
        Преобразует информацию о занятии к данному классу
        """
        day_of_week, string_day, string_time_interval = format_lesson_time(start_time, finish_time)
        return Lesson(
            number=number, day_of_week=day_of_week, string_day=string_day, string_time_interval=string_time_interval
        )

    def to_grpc_response(self) -> LessonResponse:
        return LessonResponse(
            number=self.number, day_of_week=self.day_of_week,
            string_day=self.string_day, string_time_interval=self.string_time_interval
        )


@dataclass
class Course:
    """
    Класс, описывающий курс (без занятий)
    """
    id: int
    name: str
    is_prerecorded_course: bool
    implementer: str
    roles: list[str]

    @staticmethod
    def from_model(course: CourseModel):
        """
        Преобразует объект модели БД к этому классу
        """
        roles = [role.name for role in course.roles]
        implementer = course.implementer.name
        return Course(
            id=course.id, name=course.name, is_prerecorded_course=course.is_prerecorded_course,
            implementer=implementer, roles=roles
        )

    def to_grpc_response(self) -> CourseShortResponse:
        return CourseShortResponse(id=self.id, name=self.name, is_prerecorded_course=self.is_prerecorded_course)


@dataclass
class CourseFull:
    """
    Класс, описывающий курс полностью (с занятиями)
    """
    id: int
    name: str
    description: str
    is_prerecorded_course: bool
    implementer: str
    roles: list[str]
    lessons: list[Lesson]

    @staticmethod
    def from_model(course: CourseModel):
        """
        Преобразует объект модели БД к данному классу
        """
        roles = [role.name for role in course.roles]
        implementer = course.implementer.name
        lessons = [
            Lesson.from_data(number + 1, lesson.start_time, lesson.finish_time)
            for (number, lesson) in enumerate(course.lessons)
        ]
        return CourseFull(
            id=course.id, name=course.name, description=course.description,
            is_prerecorded_course=course.is_prerecorded_course,
            implementer=implementer, roles=roles, lessons=lessons
        )

    def to_grpc_response(self) -> CourseFullResponse:
        return CourseFullResponse(
            id=self.id, name=self.name, description=self.description,
            is_prerecorded_course=self.is_prerecorded_course, implementer=self.implementer,
            roles=[role for role in self.roles],
            lessons=[lesson.to_grpc_response() for lesson in self.lessons]
        )
