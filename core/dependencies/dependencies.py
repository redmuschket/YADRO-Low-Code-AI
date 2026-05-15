from typing import Optional
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.async_db import AsyncDB
from core import config

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    from app import get_async_db, ensure_async_db_initialized
    db: AsyncDB = get_async_db()
    if db is None:
        raise RuntimeError("Database not initialized")

    await ensure_async_db_initialized()

    try:
        async for session in db.get_db():
            yield session
    except Exception as e:
        logger.error(f"Error getting the DB session: {e}", exc_info=True)
        raise