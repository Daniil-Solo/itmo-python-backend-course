from celery import Celery
from src.config import settings


celery_app = Celery('tasks', broker=settings.broker_url, backend=settings.backend_url)

celery_app.conf.update(
    enable_utc=True,
    timezone='Asia/Yekaterinburg',
)
