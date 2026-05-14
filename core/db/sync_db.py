from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from alembic import command
from alembic.config import Config as AlembicConfig
from core import logger
from core.db.config_db import ConfigDB
import core.db.models

logger = logger.get_logger(__name__)


class SyncDB:
    def __init__(self, config_db: ConfigDB):
        self.config = config_db
        self._engine = None
        self._session_local = None

    def connect(self):
        """Synchronous connection to the database."""
        try:
            engine_kwargs = self.config.sync_engine_kwargs
            session_kwargs = self.config.sync_session_kwargs

            logger.info(f"Connecting to a synchronous database: {self.config.safe_sync_url}")

            self._engine = create_engine(
                self.config.sync_database_url,
                **engine_kwargs
            )

            self._session_local = sessionmaker(
                bind=self._engine,
                **session_kwargs
            )

            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info("The synchronous database is connected")

            self.run_migrations()

        except Exception as e:
            logger.critical(f"Synchronous DATABASE connection error: {e}")
            raise

    @staticmethod
    def _run_migrations():
        """Apply migrations Alembic."""
        try:
            alembic_cfg = AlembicConfig("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            logger.info("Alembic migrations applied")
        except Exception as e:
            logger.error(f"Migration application error: {e}")
            raise

    def run_migrations(self):
        """Apply Alembic migrations."""
        try:
            alembic_cfg = AlembicConfig(str(self.config.alembic_ini_path))
            logger.info(f"Way to alembic.ini: {alembic_ini_path}")
            alembic_cfg.set_main_option('sqlalchemy.url', self.config.sync_database_url)

            command.upgrade(alembic_cfg, "head")
            logger.info("Alembic migrations applied")

        except Exception as e:
            logger.error(f"Migration application error: {e}")
            raise

    def get_session(self) -> Session:
        """Get a synchronous session."""
        if not self._session_local:
            raise RuntimeError("The database is not initialized. Call connect()")
        return self._session_local()

    def close(self):
        """Close the connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Synchronous connections are closed")