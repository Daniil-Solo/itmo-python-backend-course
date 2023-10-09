from datetime import datetime
import sqlalchemy.orm as so
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer, UniqueConstraint
from database.base import Base


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


class Student(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Студента
    Содержит информацию о имени, фамилии и табельном номере студента
    """
    __tablename__ = "students"
    firstname: so.Mapped[str] = so.mapped_column(String)
    lastname: so.Mapped[str] = so.mapped_column(String)


class CourseForStudent(Base):  # pylint: disable=too-few-public-methods
    """
    Промежуточная таблица для реализации связи многие-ко-многим для Курса и Выбора студента
    """
    __tablename__ = "course_for_students"
    student_semester_plan_id: so.Mapped[int] = so.mapped_column(ForeignKey("student_semester_plans.id"))
    course_id: so.Mapped[int] = so.mapped_column(ForeignKey("courses.id"))
    UniqueConstraint("student_semester_plan_id", "course_id")


class StudentSemesterPlan(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Выбора курсов студента на семестр
    Содержит информацию о предпочитаемой нагрузке и статус подтверждения плана
    Предпочитаемая нагрузка это количество дисциплин, которые студент собирается изучить
    """
    __tablename__ = "student_semester_plans"
    student_id: so.Mapped[int] = so.mapped_column(ForeignKey("students.id"))
    semester_load: so.Mapped[int] = so.mapped_column(Integer)
    is_confirmed: so.Mapped[bool] = so.mapped_column(Boolean, default=False)
    courses = so.relationship(Course, secondary=CourseForStudent.__tablename__)
