from sqlalchemy.ext.asyncio import AsyncSession
from auth_microservice.database.models import Base, Student
from auth_microservice.database.db import engine, DBSession
from auth_microservice.service.utils import hash_password
from auth_microservice.settings import settings


async def migrate() -> None:
    """
    Выполняет создание таблиц
    Для тестового режима сначала выполняется удаление таблиц
    """
    async with engine.begin() as conn:
        if settings.mode == "TEST":
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_students(session: AsyncSession) -> None:
    """
    Создает в БД студентов
    :param session: сессия БД
    """
    student_1 = Student(firstname="Иван", lastname="Иванов", login="i.ivanov", hashed_password=hash_password("12345"))
    student_2 = Student(firstname="Петр", lastname="Петров", login="p.petrov", hashed_password=hash_password("peter"))
    student_3 = Student(firstname="Тест", lastname="Тестовый", login="t.testov", hashed_password=hash_password("test"))
    students = [student_1, student_2, student_3]
    session.add_all(students)
    await session.commit()


async def create_data() -> None:
    """
    Заполнение БД данными
    Используется для тестирования
    """
    async with DBSession() as session:
        await create_students(session)
