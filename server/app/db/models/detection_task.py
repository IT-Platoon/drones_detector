from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import BaseTable
from app.constants import DetectionTaskStatus


class DetectionTask(BaseTable):
    __tablename__ = "detection_task"

    status = Column(
        "status",
        Enum(DetectionTaskStatus),
        default=DetectionTaskStatus.CREATED,
        nullable=False,
    )
    created_at = Column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )

    detection_items = relationship(
        "DetectionItem",
        back_populates="detection_task",
        lazy="joined",
    )
