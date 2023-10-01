from collections.abc import AsyncGenerator
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import DB_FILEPATH


DB_URL = f"sqlite+aiosqlite:///{DB_FILEPATH}"
engine = create_async_engine(DB_URL)
DBSession = async_sessionmaker(engine)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессии
    :return: сессия базы данных
    """
    async with DBSession() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise error
