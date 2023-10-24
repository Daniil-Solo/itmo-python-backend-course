import datetime
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Uuid, UUID
import sqlalchemy.orm as so
from uuid import uuid4


def generate_expire_date() -> datetime:
    return datetime.datetime.now() + datetime.timedelta(days=3)


class Base(so.DeclarativeBase):  # pylint: disable=too-few-public-methods
    """
    Базовый класс для моделей
    """
    id: so.Mapped[UUID] = so.mapped_column(
        Uuid,
        primary_key=True,
        index=True,
        default=uuid4
    )


class Student(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Студента
    Содержит информацию о имени, фамилии и табельном номере студента
    """
    __tablename__ = "students"
    firstname: so.Mapped[str] = so.mapped_column(String)
    lastname: so.Mapped[str] = so.mapped_column(String)
    login: so.Mapped[str] = so.mapped_column(String)
    hashed_password: so.Mapped[str] = so.mapped_column(String)


class Session(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Сессии
    Содержит информацию о имени, фамилии и табельном номере студента
    """
    __tablename__ = "sessions"
    student: so.Mapped[Student] = so.relationship(Student)
    student_id: so.Mapped[UUID] = so.mapped_column(ForeignKey("students.id"))
    expire_datetime: so.Mapped[datetime.datetime] = so.mapped_column(DateTime, default=generate_expire_date)
    is_active: so.Mapped[bool] = so.mapped_column(Boolean, default=True)
