from core import logger
from workers.celery_app import app
from workers.dependencies import run_async
from core.dependencies.dependencies import get_db
from core.dependencies.notification import get_processor_notification_send

from uuid6 import UUID

logger = logger.get_logger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_task(self, notification_id: UUID):
    async def _send_notification(notification_id: UUID):
        async for session in get_db():
            try:
                logger.info(f"Processing notification {notification_id}")

                # Debug: Check if get_processor_notification_send exists
                logger.info(f"get_processor_notification_send type: {type(get_processor_notification_send)}")

                processor = get_processor_notification_send(session)

                # Debug: Check what processor is
                logger.info(f"Processor type: {type(processor)}")

                if processor is None:
                    raise ValueError("get_processor_notification_send returned None")

                await processor.process(session=session, notification_id=notification_id)
                logger.info(f"Successfully processed notification {notification_id}")
                break

            except Exception as e:
                logger.error(f"Error processing notification {notification_id}: {e}", exc_info=True)
                raise

    try:
        run_async(_send_notification(notification_id))
    except Exception as exc:
        logger.error(f"Failed: {exc}", exc_info=True)
        raise self.retry(exc=exc)