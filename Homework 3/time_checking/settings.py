from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Конфигурация для микросервиса"""
    time_checking_grpc_server_address: str = Field(alias="TIME_CHECKING_ADDRESS")
    course_grpc_server_address: str = Field(alias="COURSE_ADDRESS")
    mode: str = Field(alias="MODE")


load_dotenv()
settings = Settings()
