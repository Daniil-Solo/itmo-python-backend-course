from typing import Optional
from pydantic import BaseModel, Field


class TaskCreateResponse(BaseModel):
    """
    Схема ответа для создания задачи
    """
    task_id: str


class CheckResult(BaseModel):
    """
    Схема проверки результата
    """
    status: str


class FactorialCreateRequest(BaseModel):
    """
    Схема запроса для создания задачи расчета факториала
    """
    number: int = Field(ge=1, le=10)


class CheckFactorialResult(CheckResult):
    """
    Схема ответа для создания задачи расчета числа факториала
    """
    result: Optional[int]


class FibonacciCreateRequest(BaseModel):
    """
    Схема запроса для создания задачи расчета числа Фиобоначчи
    """
    number: int = Field(ge=1, le=50)


class CheckFibonacciResult(CheckResult):
    """
    Схема ответа для создания задачи расчета числа Фиобоначчи
    """
    result: Optional[int]


class SleepCreateRequest(BaseModel):
    """
    Схема запроса для создания задачи засыпания
    """
    seconds: int = Field(ge=1, le=5)


class CheckSleepResult(CheckResult):
    """
    Схема ответа для создания задачи засыпания
    """
