from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship

from .base import BaseTable
from app.constants import DetectionItemType


class DetectionItem(BaseTable):
    __tablename__ = "detection_item"

    origin_file = Column(
        "origin_file",
        TEXT,
        nullable=False,
    )
    type = Column(
        "type",
        Enum(DetectionItemType),
        nullable=False,
    )
    predict_file = Column(
        "predict_file",
        TEXT,
        nullable=True,
    )
    classes = Column(
        "classes",
        TEXT,
        nullable=True,
    )
    detection_id = Column(
        "detection_id",
        UUID(as_uuid=True),
        ForeignKey("detection_task.id"),
        nullable=False,
    )

    detection_task = relationship(
        "DetectionTask",
        back_populates="detection_items",
        lazy="joined",
    )
