import os
from fastapi import FastAPI
from config import DB_FILEPATH
from database.data import migrate, create_data

app = FastAPI(
    title="Выбор курсов в AI Talent Hub",
    description="""API для проектирования индивидуальной образовательной траектории\
    для студентов магистратуры AI Talent Hub""",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)


@app.on_event("startup")
async def create_db():
    """
    Создает файл по пути DB_FILEPATH, который будет использоваться как БД
    Создает таблицы в БД и наполняет их данными
    """
    if not os.path.exists(DB_FILEPATH):
        await migrate()
        await create_data()
