from core import logger
from workers.celery_app import app
from workers.dependencies import run_async
from core.dependencies.dependencies import get_db
from core.dependencies.notification import get_processor_notification_send
from app.service.notification.processor.send import SendProcessor

from uuid6 import UUID

logger = logger.get_logger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_task(self, notification_id: UUID):
    async def _send_notification(notification_id: UUID):
        async for session in get_db():
            processor: SendProcessor = get_processor_notification_send(session)
            await processor.process(session, notification_id)
            break
    try:
        run_async(_send_notification(notification_id))
    except Exception as exc:
        logger.error(f"Failed: {exc}")
        raise self.retry(exc=exc)