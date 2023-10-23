import time
from src.celery_tasks.celery_app import celery_app


@celery_app.task
def factorial(number: int) -> int:
    """
    Расчет факториала
    :param number: число
    """
    def inner(value: int) -> int:
        if value == 1:
            return 1
        return inner(value-1) * value
    return inner(number)


@celery_app.task
def fibonacci(number: int) -> int:
    """
    Расчет числа Фибоначчи
    :param number: число
    """
    def inner(value: int) -> int:
        if value in (1, 2):
            return 1
        return inner(value-1) + inner(value-2)
    return inner(number)


@celery_app.task
def sleep(seconds: int) -> None:
    """
    Засыпает на определенное количество секунд
    :param seconds: количество секунд
    """
    time.sleep(seconds)
