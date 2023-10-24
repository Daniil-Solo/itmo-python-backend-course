from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer, UniqueConstraint
import sqlalchemy.orm as so


class Base(so.DeclarativeBase):  # pylint: disable=too-few-public-methods
    """
    Базовый класс для моделей
    """
    id: so.Mapped[int] = so.mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


class Role(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Роли для курса
    Примеры: Data Engineer, ML Engineer, Data Analyst и другие
    """
    __tablename__ = "roles"
    name: so.Mapped[str] = so.mapped_column(String, unique=True)


class RoleForCourse(Base):  # pylint: disable=too-few-public-methods
    """
    Промежуточная таблица для реализации связи многие-ко-многим для Курса и Роли
    """
    __tablename__ = "role_for_courses"
    course_id: so.Mapped[int] = so.mapped_column(ForeignKey("courses.id"))
    role_id: so.Mapped[int] = so.mapped_column(ForeignKey("roles.id"))
    UniqueConstraint("course_id", "role_id")


class CourseLesson(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Занятия для курса
    Содержит информацию о времени проведении занятия для не предзаписанных курсов
    """
    __tablename__ = "course_schedules"
    course_id: so.Mapped[int] = so.mapped_column(ForeignKey("courses.id"))
    start_time: so.Mapped[datetime] = so.mapped_column(DateTime)
    finish_time: so.Mapped[datetime] = so.mapped_column(DateTime)


class Implementer(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Реализатора для курса
    Примеры: ИПКН, ВШ ЦК и т.д.
    """
    __tablename__ = "implementers"
    name: so.Mapped[str] = so.mapped_column(String, unique=True)


class Course(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Курса
    Содержит информацию о названии, описании, номере семестра,
    лимите участников, предзаписанностью курса, реализаторе и ролях для курса
    """
    __tablename__ = "courses"
    name: so.Mapped[str] = so.mapped_column(String, unique=True)
    description: so.Mapped[str] = so.mapped_column(String)
    is_prerecorded_course: so.Mapped[bool] = so.mapped_column(Boolean, default=False)
    implementer_id: so.Mapped[int] = so.mapped_column(ForeignKey("implementers.id"))
    implementer: so.Mapped[Implementer] = so.relationship(Implementer)
    roles: so.Mapped[list[Role]] = so.relationship(Role, secondary=RoleForCourse.__tablename__)
    lessons: so.Mapped[list[CourseLesson]] = so.relationship(CourseLesson)

