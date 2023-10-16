from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from auth_microservice.database.db import DBSession
from auth_microservice.service.classes import Student as StudentSchema, Session as SessionSchema
from auth_microservice.database.models import Student, Session
from datetime import datetime
from uuid import UUID


class SQLAlchemyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


class AbstractStudentRepository(ABC):
    """
    Интерфейс для паттерна Репозиторий для сущности Студент
    """

    @abstractmethod
    async def get_one_by_login_and_hash_password(self, login: str, hashed_password: str) -> Optional[StudentSchema]:
        """
        Возвращает студента по логину и хэшу пароля
        """
        raise NotImplementedError


class AbstractSessionRepository(ABC):
    """
    Интерфейс для паттерна Репозиторий для сущности Сессия
    """

    @abstractmethod
    async def get_one(self, session_id: str) -> Optional[SessionSchema]:
        """
        Возвращает информацию о сессии
        """
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, user_id: str) -> SessionSchema:
        """
        Создает новую сессию
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, session_id: str, **fields) -> None:
        """
        Обновляет поле активности у сессии
        """
        raise NotImplementedError


class SQLAlchemyStudentRepository(AbstractStudentRepository, SQLAlchemyRepository):
    """
    Реализация паттерна Репозиторий для сущности Студент
    """
    async def get_one_by_login_and_hash_password(self, login: str, hashed_password: str) -> Optional[StudentSchema]:
        """
        Возвращает студента по логину и хэшу пароля
        """
        query = select(Student) \
            .where(Student.login == login) \
            .where(Student.hashed_password == hashed_password)
        result = await self.session.execute(query)
        result = result.scalar_one_or_none()
        if result is not None:
            return StudentSchema.from_model(result)


class SQLAlchemySessionRepository(AbstractSessionRepository, SQLAlchemyRepository):
    """
    Реализация паттерна Репозиторий для сущности Сессия
    """
    async def get_one(self, session_id: str) -> Optional[SessionSchema]:
        """
        Возвращает информацию о сессии
        """
        query = select(Session) \
            .where(Session.id == UUID(session_id)) \
            .where(Session.is_active) \
            .where(Session.expire_datetime <= datetime.now())
        result = await self.session.execute(query)
        result = result.scalar_one_or_none()
        if result is not None:
            return SessionSchema.from_model(result)

    async def add_one(self, user_id: str) -> SessionSchema:
        """
        Создает новую сессию
        """
        session = Session(student_id=user_id)
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return SessionSchema.from_model(session)

    async def update(self, session_id: str, **fields) -> None:
        """
        Обновляет поле активности у сессии
        """
        statement = update(Session) \
            .where(Session.id == UUID(session_id)) \
            .values(**fields)
        await self.session.execute(statement)
        await self.session.commit()


class AbstractRepositoryContextManager:
    def __init__(self):
        self.session = DBSession()

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await self.session.close()


class SessionRepositoryContextManager(AbstractRepositoryContextManager):
    async def __aenter__(self) -> SQLAlchemySessionRepository:
        return SQLAlchemySessionRepository(self.session)


class BothRepositoryContextManager(AbstractRepositoryContextManager):
    async def __aenter__(self) -> tuple[SQLAlchemySessionRepository, SQLAlchemyStudentRepository]:
        return (
            SQLAlchemySessionRepository(self.session),
            SQLAlchemyStudentRepository(self.session)
        )
