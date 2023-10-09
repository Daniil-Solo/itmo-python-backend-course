from datetime import datetime
from pydantic import BaseModel
from courses.models import Course as CourseModel, StudentSemesterPlan as PlanModel
from courses.utils import format_lesson_time


class Lesson(BaseModel):
    """
    Схема для занятия курса
    """
    number: int
    day_of_week: str
    string_day: str
    string_time_interval: str

    @staticmethod
    def from_data(number: int, start_time: datetime, finish_time: datetime):
        """
        Преобразует информацию о занятии к данной схеме
        """
        day_of_week, string_day, string_time_interval = format_lesson_time(start_time, finish_time)
        return Lesson(
            number=number, day_of_week=day_of_week, string_day=string_day, string_time_interval=string_time_interval
        )


class Course(BaseModel):
    """
    Схема для курса (без занятий)
    """
    id: int
    name: str
    is_prerecorded_course: bool
    implementer: str
    roles: list[str]

    def to_short(self):
        """
        Преобразование из полной версии курса к краткой
        """
        return CourseShort(
            id=self.id, name=self.name, is_prerecorded_course=self.is_prerecorded_course
        )

    @staticmethod
    def from_model(course: CourseModel):
        """
        Преобразует объект модели БД к данной схеме
        """
        roles = [role.name for role in course.roles]
        implementer = course.implementer.name
        return Course(
            id=course.id, name=course.name, is_prerecorded_course=course.is_prerecorded_course,
            implementer=implementer, roles=roles
        )


class CourseFull(BaseModel):
    """
    Наиболее подробная схема для курса
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
        Преобразует объект модели БД к данной схеме
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


class CourseShort(BaseModel):
    """
    Краткая версия схемы курса
    """
    id: int
    name: str
    is_prerecorded_course: bool


class SemesterPlan(BaseModel):
    """
    Схема плана изучения дисциплин
    """
    id: int
    semester_load: int
    is_confirmed: bool
    courses: list[CourseShort]

    @staticmethod
    def from_model(plan: PlanModel, use_courses=True):
        """
        Преобразует объект модели БД к данной схеме
        """
        return SemesterPlan(
            id=plan.id, semester_load=plan.semester_load, is_confirmed=plan.is_confirmed,
            courses=[
                CourseShort(id=c.id, name=c.name, is_prerecorded_course=c.is_prerecorded_course)
                for c in plan.courses] if use_courses else []
        )


class SemesterPlanCreate(BaseModel):
    """
    Схема для создания плана изучения дисциплин
    """
    semester_load: int


class OperationResult(BaseModel):
    """
    Схема для результата операции
    """
    is_successful: bool
    message: str
