from enum import Enum
from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    """
    Роль в проекте, на которую рассчитан курс
    """
    DE = 'Data Engineer'
    MLE = 'Machine Learning Engineer'
    DA = 'Data Analyst'
    A = 'AI Architect'
    PM = 'AI Product Manager'


class Implementer(str, Enum):
    """
    Реализатор курса
    """
    IPKN = 'ИПКН'
    PISH = 'ПИШ'
    WSH_CK = 'ВШ ЦК'
    OTHER = 'Другое'


class Course(BaseModel):
    """
    Информация о курсе
    """
    id: int
    title: str
    roles: list[Role]
    implementer: Implementer


class CourseRequest(BaseModel):
    """
    Заявка студента на курс
    """
    student_email: EmailStr
    student_number: int
    course_id: int
    student_motivation: str = ""


class CourseRequestAnswer(BaseModel):
    """
    Ответ на заявку студента на курс. Сделан для документации API
    """
    message: str
