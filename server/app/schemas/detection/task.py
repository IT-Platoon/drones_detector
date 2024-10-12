import datetime
import uuid

from pydantic import BaseModel

from .item import DetectionItemBase
from app.constants import DetectionTaskStatus


class DetectionTaskBase(BaseModel):
    id: uuid.UUID
    status: DetectionTaskStatus
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class DetectionTaskCompleted(DetectionTaskBase):
    detection_items: list[DetectionItemBase]
