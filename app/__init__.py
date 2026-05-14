from core import logger
from flask import Flask
import os

from core import config
from core.db.async_db import AsyncDB
from core.db.sync_db import SyncDB
from app.http.middeleware import register_all_middleware
from app.http.route.notification import notification_bp

logger = logger.get_logger(__name__)

sync_db_instance = None
async_db_instance = None


def register_blueprints(app: Flask):
    app.register_blueprint(notification_bp)
    logger.debug("Blueprint'ы registered")

def init_sync_db(app: Flask):
    global sync_db_instance

    sync_db_instance = SyncDB(config.db_config)
    try:
        sync_db_instance.connect()
        app.extensions['sync_db'] = sync_db_instance
        logger.info("The synchronous database object has been created (connection in workshops)")
        logger.info("The database is connected")
    except Exception as e:
        logger.critical(f"Error connecting to the database: {e}")
        raise

def init_async_db(app: Flask):
    global async_db_instance
    async_db_instance = AsyncDB(config.db_config)
    app.extensions['async_db'] = async_db_instance
    logger.info("Asynchronous database object created (connection in workshops)")

def get_sync_db():
    if sync_db_instance is None:
        logger.error("The synchronous database is not initialized")
        raise RuntimeError("The synchronous database is not initialized")
    return sync_db_instance

def get_async_db():
    if async_db_instance is None:
        logger.error("Asynchronous database is not initialized")
        raise RuntimeError("Asynchronous database is not initialized")
    return async_db_instance

def create_app():
    global async_db_instance
    app = Flask(__name__)


    register_blueprints(app)
    init_sync_db(app)
    init_async_db(app)
    register_all_middleware(app)

    logger.info("Flask app created")
    return app

app = create_app()

__all__ = ["app", "get_sync_db", "get_async_db"]