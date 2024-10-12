from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from app.db.models import DetectionItem
from app.schemas.detection import DetectionItemCreate
from app.services import FileStorageService


class DetectionItemRepository(BaseRepository[DetectionItem, DetectionItemCreate, None]):
    def __init__(self):
        super().__init__(DetectionItem)

    async def remove(self, session: AsyncSession, *, obj_id: int):
        obj = await self.get(session, obj_id=obj_id)
        await session.delete(obj)
        await session.commit()

    async def get_by_detection_id(self, session: AsyncSession, *, detection_id: str):
        query = select(self.model).filter(self.model.detection_id == detection_id)
        result = await session.execute(query)
        return result.scalars().all()
