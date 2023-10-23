from fastapi import FastAPI
from src.router import task_router

app = FastAPI(
    title="Использование очереди сообщений",
    description='Пример использования очереди сообщений для выполнения "тяжелых" задач',
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)


app.include_router(router=task_router, prefix="/tasks")
