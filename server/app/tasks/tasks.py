import asyncio

from app.config import celery_app
from app.services import YOLOWrapper
from app.utils.celery import run_detection as run_detection_async


model = YOLOWrapper(path="./app/services/model/weights/best.pt", conf=0.45, iou=0.5)


@celery_app.task
def run_detection(uuid: str):
    asyncio.run(run_detection_async(uuid, model))
