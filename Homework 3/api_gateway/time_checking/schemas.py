from pydantic import BaseModel


class CourseList(BaseModel):
    """
    Схема для списка идентификаторов курсов
    """
    items: list[int]


class OperationResult(BaseModel):
    """
    Схема для результата операции
    """
    is_successful: bool
    message: str
