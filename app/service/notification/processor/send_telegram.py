from core.domain.notification import Notification
from core import logger

logger = logger.get_logger(__name__)


class SendTelegramProcessor:
    async def push(self, notification: Notification):
        notification.mark_as_sent()
        logger.info(f'Send telegram notification: {str(notification.id)}')