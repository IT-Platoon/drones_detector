from datetime import datetime, timedelta

from sqlalchemy import select

from .base import BaseRepository
from app.db.models import DetectionTask


class DetectionTaskRepository(BaseRepository[DetectionTask, None, None]):
    def __init__(self):
        super().__init__(DetectionTask)

    async def get_old_tasks(self, session, *, different_time: timedelta = timedelta(days=1)):
        now = datetime.now()
        query = select(self.model).filter((now - self.model.created_at) >= different_time)
        result = await session.execute(query)
        return result.scalars().unique()
