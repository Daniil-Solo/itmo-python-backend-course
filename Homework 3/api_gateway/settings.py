from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    course_grpc_server_address: str = Field(alias="COURSE_ADDRESS")
    auth_grpc_server_address: str = Field(alias="AUTH_ADDRESS")
    student_planning_grpc_server_address: str = Field(alias="STUDENT_PLANNING_ADDRESS")


load_dotenv()
settings = Settings()
