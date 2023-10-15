from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    course_grpc_server_address: str = Field(alias="COURSE_ADDRESS")
    db_filepath: str = Field(alias="COURSE_DB_FILEPATH")
    mode: str = Field(alias="MODE")


load_dotenv()
settings = Settings()
