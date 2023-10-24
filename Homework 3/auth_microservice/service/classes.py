from uuid import uuid4
from dataclasses import dataclass
from auth_microservice.database.models import (
    Student as StudentModel, Session as SessionModel
)


@dataclass
class Session:
    id: uuid4
    student_id: uuid4
    expire_timestamp: float
    is_active: bool

    @staticmethod
    def from_model(session: SessionModel):
        return Session(
            id=session.id, student_id=session.student_id,
            expire_timestamp=session.expire_datetime.timestamp(), is_active=session.is_active
        )


@dataclass
class Student:
    id: uuid4

    @staticmethod
    def from_model(student: StudentModel):
        return Student(id=student.id)
