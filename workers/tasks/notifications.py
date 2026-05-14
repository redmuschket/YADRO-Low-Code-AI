import asyncio

from workers.celery_app import app
from core import logger

logger = logger.get_logger(__name__)


async def _async_send(notification_id: int):
    logger.info(f"The beginning of sending the notification #{notification_id}")
    await asyncio.sleep(1)
    logger.info(f"Notification #{notification_id} shipped")


def _run_async(coro):
    """Launching asynchronous coroutines."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_task(self, notification_id: int):
    """
    Celery's task is to send a notification.
    Called from Flask: send_notification_task.delay(notification_id)
    """
    try:
        logger.info(f"Task: sending a notification #{notification_id}")
        _run_async(_async_send(notification_id))
        return f"ОК: #{notification_id}"
    except Exception as exc:
        logger.error(f"Sending error #{notification_id}: {exc}")
        raise self.retry(exc=exc)