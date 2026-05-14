from core import logger
from workers.celery_app import app
from workers.dependencies import run_async
from core.dependencies.dependencies import get_db
from core.dependencies.notification import get_async_notification_service

from uuid6 import UUID

logger = logger.get_logger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_task(self, notification_id: UUID):
    async def _send_notification(notification_id: UUID):
        async for session in get_db():
            service = get_async_notification_service(session)
            await service.send(notification_id)
            break
    try:
        run_async(_send_notification(notification_id))
        return f"OK: #{notification_id}"
    except Exception as exc:
        logger.error(f"Failed: {exc}")
        raise self.retry(exc=exc)