from fastapi import APIRouter, status, Body, Path
from src.schemas import (
    TaskCreateResponse,
    FactorialCreateRequest, CheckFactorialResult,
    FibonacciCreateRequest, CheckFibonacciResult,
    SleepCreateRequest, CheckSleepResult
)
from src.celery_tasks.tasks import factorial, fibonacci, sleep
from src.celery_tasks.celery_app import celery_app


task_router = APIRouter(tags=["Тяжелые задачи"])


@task_router.post("/factorial", status_code=status.HTTP_201_CREATED, response_model=TaskCreateResponse,
                  description="Рассчитывает факториал числа в пределах от 1 до 100")
def calculate_factorial(data: FactorialCreateRequest = Body()):
    """
    Рассчитывает факториал числа в пределах от 1 до 100
    :param data: число для расчета
    :return: идентификатор задачи
    """
    task = factorial.delay(data.number)
    return TaskCreateResponse(task_id=str(task))


@task_router.get("/factorial/{task_id:str}", response_model=CheckFactorialResult,
                 description="Проверяет статус выполнения текущей задачи и возвращает её результат")
def check_factorial(task_id: str = Path()):
    """
    Проверяет статус выполнения текущей задачи и возвращает её результат
    :param task_id: идентификатор задачи
    :return: статус и значение
    """
    task = celery_app.AsyncResult(task_id)
    result = task.get() if task.state == 'SUCCESS' else None
    return CheckFactorialResult(status=task.state, result=result)


@task_router.post("/fibonаcci", status_code=status.HTTP_201_CREATED, response_model=TaskCreateResponse,
                  description="Рассчитывает число Фибоначчи в пределах от 1 до 500")
def calculate_fibonacci(data: FibonacciCreateRequest = Body()):
    """
    Рассчитывает число Фибоначчи в пределах от 1 до 500
    :param data: число для расчета
    :return: идентификатор задачи
    """
    task = fibonacci.delay(data.number)
    return TaskCreateResponse(task_id=str(task))


@task_router.get("/fibonаcci/{task_id:str}", response_model=CheckFibonacciResult,
                 description="Проверяет статус выполнения текущей задачи и возвращает её результат")
def check_fibonacci(task_id: str = Path()):
    """
    Проверяет статус выполнения текущей задачи и возвращает её результат
    :param task_id: идентификатор задачи
    :return: статус и значение
    """
    task = celery_app.AsyncResult(task_id)
    result = task.get() if task.state == 'SUCCESS' else None
    return CheckFibonacciResult(status=task.state, result=result)


@task_router.post("/sleep", status_code=status.HTTP_201_CREATED, response_model=TaskCreateResponse,
                  description="Выполняет тяжелую задачу на определенное количество секунд")
def start_sleeping(data: SleepCreateRequest = Body()):
    """
    Выполняет тяжелую задачу на определенное количество секунд
    :param data: количество секунд
    :return: идентификатор задачи
    """
    task = sleep.delay(data.seconds)
    return TaskCreateResponse(task_id=str(task))


@task_router.get("/sleep/{task_id:str}", response_model=CheckSleepResult,
                 description="Проверяет статус выполнения текущей задачи")
def check_sleeping(task_id: str = Path()):
    """
    Проверяет статус выполнения текущей задачи
    :param task_id: идентификатор задачи
    :return: статус
    """
    task = celery_app.AsyncResult(task_id)
    result = task.get() if task.state == 'SUCCESS' else None
    return CheckSleepResult(status=task.state, result=result)
