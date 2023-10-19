import pytest
from datetime import datetime
from course_microservice.service.utils import stringify_time, get_string_day


@pytest.mark.parametrize(
    ("some_time", "expected"), [
        (datetime(day=1, month=1, year=2001, hour=12, minute=30), "12:30"),
        (datetime(day=23, month=11, year=2023, hour=3, minute=9), "3:09"),
        (datetime(day=10, month=10, year=2010, hour=23, minute=0), "23:00"),
    ]
)
def test_getting_string_time(some_time, expected):
    assert stringify_time(some_time) == expected


@pytest.mark.parametrize(
    ("some_time", "expected"), [
        (datetime(day=9, month=11, year=2023, hour=12, minute=30), "9 ноября 2023 года"),
        (datetime(day=29, month=1, year=2022, hour=3, minute=9), "29 января 2022 года"),
        (datetime(day=6, month=6, year=2010, hour=23, minute=0), "6 июня 2010 года"),
    ]
)
def test_getting_string_day(some_time, expected):
    assert get_string_day(some_time) == expected
