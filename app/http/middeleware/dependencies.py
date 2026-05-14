from flask import g

from core.dependencies.notification import get_notification_service
from core import logger

logger = logger.get_logger(__name__)


def register_dependencies_middleware(app):
    @app.before_request
    def inject_dependencies():
        if hasattr(g, 'db_session'):
            g.notification_service = get_notification_service(g.db_session)