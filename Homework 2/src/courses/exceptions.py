from fastapi import status


class CourseException(Exception):
    """
    Исключение-родитель для исключений модуля
    """
    STATUS = status.HTTP_400_BAD_REQUEST


class NoSuchCourseException(CourseException):
    """
    Исключение: нет такого курса
    """
    STATUS = status.HTTP_404_NOT_FOUND


class NoSuchStudentException(CourseException):
    """
    Исключение: нет такого студента
    """
    STATUS = status.HTTP_404_NOT_FOUND


class SemesterPlanForSuchStudentExistsException(CourseException):
    """
    Исключение: план на семестр для такого студента уже существует
    """


class SemesterPlanForSuchStudentDoesntExistsException(CourseException):
    """
    Исключение: нет плана на семестр для такого студента
    """
    STATUS = status.HTTP_404_NOT_FOUND
