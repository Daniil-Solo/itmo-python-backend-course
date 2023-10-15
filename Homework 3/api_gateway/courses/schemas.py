from pydantic import BaseModel


class Lesson(BaseModel):
    """
    Схема для занятия курса
    """
    number: int
    day_of_week: str
    string_day: str
    string_time_interval: str


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


class CourseShort(BaseModel):
    """
    Краткая версия схемы курса
    """
    id: int
    name: str
    is_prerecorded_course: bool
