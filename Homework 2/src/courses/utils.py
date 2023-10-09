import locale
from datetime import datetime
from courses.constants import MONTH_MAPPING


locale.setlocale(locale.LC_TIME, 'Russian')


def stringify_time(time: datetime) -> str:
    """
    Приводит объект даты и времени к строчному виду: часы:минуты
    Примеры выводов: 18:30, 9:41
    """
    return time.strftime("%H:%M").lstrip("0")


def get_day_of_week(time: datetime) -> str:
    """
    Приводит объект даты и времени к русскому названию дня недели
    Примеры выводов: Понедельник, Суббота
    """
    return time.strftime("%A").capitalize()


def get_string_day(time: datetime) -> str:
    """
    Приводит объект даты и времени к строчному виду: день месяц в родительном падеже год
    Примеры выводов: 12 октября 2023 года, 9 ноября 2023 года
    """
    return time.strftime("%d").lstrip("0") + " " + MONTH_MAPPING[time.month] + " " + time.strftime("%Y") + " года"


def format_lesson_time(start_time: datetime, finish_time: datetime) -> tuple[str, str, str]:
    """
    Приводит объекты даты и времени начала и конца занятия к строчному виду
    Пример вывода: Понедельник, 12 октября 2023 года, 16:40 - 18:30
    """
    day_of_week = get_day_of_week(start_time)
    string_day = get_string_day(start_time)
    string_time_interval = stringify_time(start_time) + " - " + stringify_time(finish_time)
    return day_of_week, string_day, string_time_interval
