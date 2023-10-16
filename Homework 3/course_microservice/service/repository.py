from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from course_microservice.database.db import DBSession
from course_microservice.service.classes import Course as CourseSchema, CourseFull as CourseFullSchema
from course_microservice.database.models import Course


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

    @abstractmethod
    async def exists(self, course_id) -> bool:
        """
        Проверяет существование курса
        """
        raise NotImplementedError


class SQLAlchemyCourseRepository(AbstractCourseRepository):
    """
    Конкретная реализация паттерна Репозиторий для сущности Курс
    """
    def __init__(self, session: AsyncSession):
        self.session = session

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

    async def one(self, course_id: int) -> Optional[CourseFullSchema]:
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

    async def exists(self, course_id: int) -> bool:
        """
        Проверяет существование курса
        """
        query = select(Course).where(Course.id == course_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None


class CourseRepositoryContextManager:
    def __init__(self):
        self.session = DBSession()

    async def __aenter__(self):
        return SQLAlchemyCourseRepository(self.session)

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await self.session.close()
