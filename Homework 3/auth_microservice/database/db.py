from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from auth_microservice.settings import settings


db_url = f"sqlite+aiosqlite:///{settings.db_filepath}"
engine = create_async_engine(db_url)
DBSession = async_sessionmaker(engine)
