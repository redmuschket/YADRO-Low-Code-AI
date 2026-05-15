from core import logger
from workers.celery_app import app
from workers.dependencies import run_async
from core.dependencies.dependencies import get_db
from core.dependencies.notification import get_processor_notification_send, get_async_notification_service

from uuid6 import UUID

logger = logger.get_logger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_task(self, notification_id: UUID):
    async def _send_notification(notification_id: UUID):
        async for session in get_db():
            service = get_async_notification_service(session)
            try:
                logger.info(f"Processing notification {notification_id}")
                processor = get_processor_notification_send(session)

                await processor.process(session=session, notification_id=notification_id)
                logger.info(f"Successfully processed notification {notification_id}")
                break

            except Exception as e:
                logger.error(f"Error processing notification {notification_id}: {e}", exc_info=True)
                if self.request.retries >= self.max_retries:
                    logger.error(f"Max retries reached for notification {notification_id}, marking as FAILED")
                    notification = service.get_notification_by_id(notification_id)
                    notification.status = NotificationStatus.FAILED
                    service.update(notification)
                    logger.info(f"Notification {notification_id} status updated to FAILED")
                raise

    try:
        run_async(_send_notification(notification_id))
    except Exception as exc:
        logger.error(f"Failed: {exc}", exc_info=True)
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        else:
            logger.error(f"Task failed after {self.max_retries} retries: {notification_id}")