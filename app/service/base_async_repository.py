from sqlalchemy.ext.asyncio import AsyncSession
from app.service.base_repository import BaseRepository


class AsyncRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def _flush(self):
        await self._db.flush()