import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from config import DB_FILEPATH
from courses.router import course_router, choice_router
from courses.exceptions import CourseException
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
    Создает файл по пути DB_FILEPATH, который будет использоваться как БД.
    Создает таблицы в БД и наполняет их данными.
    """
    if not os.path.exists(DB_FILEPATH):
        await migrate()
        await create_data()


@app.exception_handler(CourseException)
async def handle_course_exceptions(_: Request, ex: CourseException):
    """
    Обрабатывает ошибки из модуля courses, связанные с отсутствием сущностей в базе данных
    """
    return JSONResponse({"message": str(ex)}, status_code=ex.STATUS)


app.include_router(course_router, prefix="/courses")
app.include_router(choice_router, prefix="/semester_plan")
