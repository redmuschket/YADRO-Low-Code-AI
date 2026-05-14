from typing import Optional
from fastapi import Request
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.async_db import AsyncDB
from core import config

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    from app import get_async_db
    db: AsyncDB = get_async_db()
    if db is None:
        raise RuntimeError("Database not initialized")
    async for session in db.get_db():
        yield session
