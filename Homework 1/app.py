from fastapi import FastAPI
from router import course_router


app = FastAPI(
    title="Выбор курсов в AI Talent Hub",
    description="""API для проектирования индивидуальной образовательной траектории\
    для студентов магистратуры AI Talent Hub""",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)


app.include_router(router=course_router, prefix="/courses")
