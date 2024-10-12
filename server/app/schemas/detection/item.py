import uuid

from pydantic import BaseModel

from app.constants import DetectionItemType


class DetectionItemCreate(BaseModel):
    origin_file: str
    type: DetectionItemType
    detection_id: uuid.UUID


class DetectionItemBase(DetectionItemCreate):
    id: uuid.UUID
    predict_file: str | None
    classes: str | None

    class Config:
        orm_mode = True
