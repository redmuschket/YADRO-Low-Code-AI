from flask import g

from core import logger

logger = logger.get_logger(__name__)


def register_database_middleware(app):
    @app.before_request
    def open_db_session():
        from app import get_sync_db
        db = get_sync_db()
        g.db_session = db.get_session()
        logger.debug("The database session is open")

    @app.teardown_request
    def close_db_session(exception=None):
        db_session = g.pop('db_session', None)
        if db_session:
            db_session.close()
            logger.debug("The database session is closed")