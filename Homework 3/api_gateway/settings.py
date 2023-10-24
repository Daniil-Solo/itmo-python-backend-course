from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Конфигурация для микросервиса"""
    course_grpc_server_address: str = Field(alias="COURSE_ADDRESS")
    auth_grpc_server_address: str = Field(alias="AUTH_ADDRESS")
    time_checking_grpc_server_address: str = Field(alias="TIME_CHECKING_ADDRESS")


load_dotenv()
settings = Settings()
