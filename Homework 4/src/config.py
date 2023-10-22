from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    """Конфиг для проекта"""
    broker_url: str = Field(alias="BROKER_URL")
    backend_url: str = Field(alias="BACKEND_URL")


settings = Settings()
