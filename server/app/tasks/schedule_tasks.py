import asyncio

from app.config import celery_app
from app.utils.celery import remove_old_detections as remove_old_detections_async


@celery_app.task
def remove_old_detections():
    asyncio.run(remove_old_detections_async())
