from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload
from courses.schemas import Course as CourseSchema, CourseFull as CourseFullSchema, \
    SemesterPlanCreate as SemesterPlanCreateSchema, SemesterPlan as SemesterPlanSchema
from courses.models import Course, StudentSemesterPlan, Student, CourseForStudent


class SQLAlchemyRepository(ABC):  # pylint: disable=too-few-public-methods
    """
    Миксин для классов, использующих SQLAlchemy
    """
    def __init__(self, session: AsyncSession):
        self.session = session


class AbstractCourseRepository(ABC):
    """
    Интерфейс для паттерна Репозиторий для сущности Курс
    """
    @abstractmethod
    async def list(self) -> list[CourseSchema]:
        """
        Возвращает список курсов
        """
        raise NotImplementedError

    @abstractmethod
    async def one(self, course_id) -> Optional[CourseFullSchema]:
        """
        Возвращает подробную информацию о курсе
        """
        raise NotImplementedError


class SQLAlchemyCourseRepository(SQLAlchemyRepository, AbstractCourseRepository):
    """
    Конкретная реализация паттерна Репозиторий для сущности Курс
    """
    async def list(self) -> list[CourseSchema]:
        """
        Возвращает список курсов
        """
        query = select(Course)\
            .options(
                joinedload(Course.roles),
                joinedload(Course.implementer)
        )
        result = await self.session.execute(query)
        courses = result.unique().scalars().all()
        return [CourseSchema.from_model(course) for course in courses]

    async def one(self, course_id) -> Optional[CourseFullSchema]:
        """
        Возвращает подробную информацию о курсе
        """
        query = select(Course) \
            .where(Course.id == course_id)\
            .options(
                joinedload(Course.roles),
                joinedload(Course.implementer),
                joinedload(Course.lessons)
        )
        result = await self.session.execute(query)
        course = result.unique().scalar_one_or_none()
        if course is not None:
            return CourseFullSchema.from_model(course)


class AbstractSemesterPlanRepository(ABC):
    """
    Интерфейс для паттерна Репозиторий для сущности План для изучения дисциплин
    """
    @abstractmethod
    async def add_one(self, student_id: int, semester_plan: SemesterPlanCreateSchema) -> SemesterPlanSchema:
        """
        Создает новый план для изучения дисциплин студента
        """
        raise NotImplementedError

    @abstractmethod
    async def one(self, student_id: int) -> Optional[SemesterPlanSchema]:
        """
        Возвращает подробную информацию о плане студента
        """
        raise NotImplementedError

    @abstractmethod
    async def add_course(self, course_id: int, semester_plan_id: int) -> None:
        """
        Добавляет курс в план
        """
        raise NotImplementedError

    @abstractmethod
    async def remove_course(self, course_id: int, semester_plan_id: int) -> None:
        """
        Удаляет курс из плана
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, semester_plan_id: int, **updating_values) -> None:
        """
        Изменяет план
        """
        raise NotImplementedError


class SQLAlchemySemesterPlanRepository(SQLAlchemyRepository, AbstractSemesterPlanRepository):
    """
    Конкретная реализация паттерна Репозиторий для сущности План для изучения дисциплин
    Для того чтобы не создавать новый Репозиторий, добавил в этот же класс методы для добавления и удаления курсов
    """
    async def add_one(self, student_id: int, semester_plan: SemesterPlanCreateSchema) -> SemesterPlanSchema:
        """
        Создает новый план для изучения дисциплин студента
        """
        student_plan = StudentSemesterPlan(
            student_id=student_id,
            semester_load=semester_plan.semester_load
        )
        self.session.add(student_plan)
        await self.session.commit()
        await self.session.refresh(student_plan)
        return SemesterPlanSchema.from_model(student_plan, use_courses=False)

    async def one(self, student_id: int) -> Optional[SemesterPlanSchema]:
        """
        Возвращает подробную информацию о плане студента
        """
        query = select(StudentSemesterPlan) \
            .options(
                joinedload(StudentSemesterPlan.courses)
            )\
            .where(StudentSemesterPlan.student_id == student_id)
        result = await self.session.execute(query)
        plan = result.unique().scalar_one_or_none()
        if plan is not None:
            return SemesterPlanSchema.from_model(plan)

    async def add_course(self, course_id: int, semester_plan_id: int) -> None:
        """
        Добавляет курс в план
        """
        course_for_student = CourseForStudent(
            student_semester_plan_id=semester_plan_id,
            course_id=course_id
        )
        self.session.add(course_for_student)
        await self.session.commit()

    async def remove_course(self, course_id: int, semester_plan_id: int) -> None:
        """
        Удаляет курс из плана
        """
        statement = delete(CourseForStudent)\
            .where(CourseForStudent.course_id == course_id)\
            .where(CourseForStudent.student_semester_plan_id == semester_plan_id)
        await self.session.execute(statement)
        await self.session.commit()

    async def update(self, semester_plan_id: int, **updating_values) -> None:
        """
        Изменяет план
        """
        statement = update(StudentSemesterPlan)\
            .where(StudentSemesterPlan.id == semester_plan_id)\
            .values(**updating_values)
        await self.session.execute(statement)
        await self.session.commit()


class AbstractStudentRepository(ABC):  # pylint: disable=too-few-public-methods
    """
    Интерфейс для паттерна Репозиторий для сущности Студент
    """
    @abstractmethod
    async def exists(self, student_id: int) -> bool:
        """
        Проверяет существование студента
        """
        raise NotImplementedError


class SQLAlchemyStudentRepository(SQLAlchemyRepository, AbstractStudentRepository):  # pylint: disable=too-few-public-methods
    """
    Конкретная реализация паттерна Репозиторий для сущности Студент
    """
    async def exists(self, student_id: int) -> bool:
        """
        Проверяет существование студента
        """
        query = select(Student).where(Student.id == student_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
