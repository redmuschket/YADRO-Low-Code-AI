from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from core import logger
from core.db.config_db import ConfigDB

logger = logger.get_logger(__name__)
Base = declarative_base()


class DB:
    def __init__(self, config_db: ConfigDB):
        self.config = config_db
        self._engine = None
        self._async_session_local = None

    async def init_db_client(self):
        """Initializing an asynchronous connection."""
        try:
            engine_kwargs = self.config.async_engine_kwargs
            session_kwargs = self.config.async_session_kwargs

            logger.info(f"Connecting to the database: {self.config.safe_async_url}")
            logger.debug(f"Engine Parameters: {engine_kwargs}")
            logger.debug(f"Session parameters: {session_kwargs}")

            self._engine = create_async_engine(
                self.config.async_database_url,
                **engine_kwargs
            )

            self._async_session_local = async_sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                **session_kwargs
            )

            import core.db.models

            try:
                async with self._engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
            except ConnectionRefusedError:
                raise
            except Exception as e:
                logger.error(f"Error when creating tables: {type(e).__name__}")
                raise

        except ConnectionRefusedError:
            raise
        except Exception as e:
            logger.error(f"Critical error during DB initialization: {type(e).__name__}")
            raise

    async def close_db_client(self):
        """Closing connections."""
        if self._engine:
            await self._engine.dispose()
            logger.info("DB connection closed")

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Returns an asynchronous session."""
        async with self._async_session_local() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                try:
                    await session.close()
                except Exception:
                    pass