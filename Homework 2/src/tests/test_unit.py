from typing import Optional
from datetime import datetime
import pytest
from courses.repositories import AbstractCourseRepository
from courses.schemas import Course as CourseSchema, CourseFull as CourseFullSchema, CourseShort, Lesson
from courses.constants import Implementer, Role
from courses.services import CourseService, StudentChoiceService
from courses.utils import get_string_day


class FakeCourseRepository(AbstractCourseRepository):
    """
    Для целей тестирования реализован только метод list
    """
    def __init__(self):
        self.storage = [
            CourseSchema(
                id=1, name="Курс 1", is_prerecorded_course=True, implementer=Implementer.PISH, roles=[Role.A, Role.MLE]
            ),
            CourseSchema(
                id=2, name="Курс 2", is_prerecorded_course=True, implementer=Implementer.IPKN, roles=[Role.DE, Role.MLE]
            ),
            CourseSchema(
                id=3, name="Курс 3", is_prerecorded_course=False, implementer=Implementer.WSH_CK, roles=[Role.DA]
            ),
            CourseSchema(
                id=4, name="Курс 11", is_prerecorded_course=False, implementer=Implementer.PISH, roles=[Role.DE]
            ),
            CourseSchema(
                id=5, name="Курс 13", is_prerecorded_course=False, implementer=Implementer.IPKN, roles=[Role.DA, Role.A]
            ),
        ]

    async def list(self) -> list[CourseSchema]:
        return self.storage

    async def one(self, course_id) -> Optional[CourseFullSchema]:
        return None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('implementer', 'role', 'search', 'expected'), [
        (
                Implementer.PISH, None, None,
                [
                    CourseShort(id=1, name="Курс 1", is_prerecorded_course=True),
                    CourseShort(id=4, name="Курс 11", is_prerecorded_course=False)
                ]
        ),
        (
                Implementer.PISH, Role.A, None,
                [
                    CourseShort(id=1, name="Курс 1", is_prerecorded_course=True)
                ]
        ),
        (
                Implementer.PISH, Role.A, "2", []
        ),
        (
                None, None, "Не курс", []
        ),
        (
                None, None, "13", [CourseShort(id=5, name="Курс 13", is_prerecorded_course=False)]
        ),
    ]
)
async def test_course_filtering(implementer, role, search, expected):
    """Тестирование поиска курсов по фильтрам"""
    course_repo = FakeCourseRepository()
    course_service = CourseService(course_repo)
    assert await course_service.get_courses(implementer, role, search) == expected


@pytest.mark.parametrize(
    ("some_time", "expected"), [
        (datetime(day=1, month=1, year=2001, hour=12, minute=30), "1 января 2001 года"),
        (datetime(day=23, month=11, year=2023, hour=3, minute=9), "23 ноября 2023 года"),
        (datetime(day=10, month=10, year=2010, hour=10, minute=10), "10 октября 2010 года"),
    ]
)
def test_getting_string_day(some_time, expected):
    """Тестирование получения строкового представления дня"""
    assert get_string_day(some_time) == expected


COURSES_FOR_TIME_CHECKING = [
    CourseFullSchema(
        id=1, name="1", description="1", is_prerecorded_course=True,
        implementer="1", roles=[], lessons=[
            Lesson(number=1, day_of_week="Пн", string_day="21 октября 2023 года", string_time_interval="9:00 - 10:30"),
            Lesson(number=2, day_of_week="Ср", string_day="23 октября 2023 года", string_time_interval="9:00 - 10:30"),
            Lesson(number=3, day_of_week="ПН", string_day="28 октября 2023 года", string_time_interval="9:00 - 10:30"),
        ]
    ),
    CourseFullSchema(
        id=2, name="2", description="2", is_prerecorded_course=True,
        implementer="2", roles=[], lessons=[
            Lesson(number=1, day_of_week="Пн", string_day="21 октября 2023 года", string_time_interval="10:40 - 13:00"),
            Lesson(number=2, day_of_week="Ср", string_day="23 октября 2023 года", string_time_interval="10:40 - 13:00"),
        ]
    ),
    CourseFullSchema(
        id=3, name="3", description="3", is_prerecorded_course=True,
        implementer="3", roles=[], lessons=[
            Lesson(number=1, day_of_week="Вт", string_day="22 октября 2023 года", string_time_interval="9:00 - 10:30"),
            Lesson(number=2, day_of_week="ПН", string_day="23 октября 2023 года", string_time_interval="10:40 - 13:00"),
        ]
    ),
]


@pytest.mark.parametrize(
    ("courses", "adding_course", "expected"), [
        (  # полный дубль
                COURSES_FOR_TIME_CHECKING,
                CourseFullSchema(
                    id=4, name="4", description="4", is_prerecorded_course=True,
                    implementer="4", roles=[], lessons=[
                        Lesson(number=1, day_of_week="Вт", string_day="22 октября 2023 года",
                               string_time_interval="9:00 - 10:30"),
                        Lesson(number=2, day_of_week="Вт", string_day="23 октября 2023 года",
                               string_time_interval="10:40 - 13:00"),
                    ]
                ), False
        ),
        (  # частичный дубль
                COURSES_FOR_TIME_CHECKING,
                CourseFullSchema(
                    id=4, name="4", description="4", is_prerecorded_course=True,
                    implementer="4", roles=[], lessons=[
                        Lesson(number=1, day_of_week="ПН", string_day="22 октября 2023 года",
                               string_time_interval="9:00 - 10:30"),
                        Lesson(number=2, day_of_week="Вт", string_day="23 октября 2023 года",
                               string_time_interval="15:30 - 17:00"),
                    ]
                ), False
        ),
        (  # другой день и другое время
                COURSES_FOR_TIME_CHECKING,
                CourseFullSchema(
                    id=4, name="4", description="4", is_prerecorded_course=True,
                    implementer="4", roles=[], lessons=[
                        Lesson(number=1, day_of_week="Вс", string_day="27 октября 2023 года",
                               string_time_interval="9:00 - 10:30"),
                        Lesson(number=2, day_of_week="Вт", string_day="29 октября 2023 года",
                               string_time_interval="10:40 - 13:00"),
                    ]
                ), True
        ),
        (  # тот же день и другое время
                COURSES_FOR_TIME_CHECKING,
                CourseFullSchema(
                    id=4, name="4", description="4", is_prerecorded_course=True,
                    implementer="4", roles=[], lessons=[
                        Lesson(number=1, day_of_week="Пн", string_day="22 октября 2023 года",
                               string_time_interval="13:10 - 15:00"),
                        Lesson(number=2, day_of_week="Вт", string_day="23 октября 2023 года",
                               string_time_interval="7:20 - 8:50"),
                    ]
                ), True
        ),
    ]
)
def test_check_time_for_course(courses, adding_course, expected):
    """Тестирование проверки времени на изучение курса при условии что уже какие-то курсы выбраны"""
    assert StudentChoiceService.has_time_for_course(courses, adding_course) == expected
