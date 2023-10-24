import datetime

from pydantic import BaseModel


class Login(BaseModel):
    """
    Схема для входа в систему
    """
    login: str
    password: str


class Session(BaseModel):
    """
    Схема для сессии
    """
    id: str
    expire_date: datetime.datetime


class OperationResponse(BaseModel):
    """
    Схема для результата операции
    """
    message: str
