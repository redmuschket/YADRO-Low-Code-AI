from core import logger
from app.service.notification.async_notification import AsyncNotificationService
from app.service.notification.processor.send_email import SendEmail
from app.service.notification.processor.send_sms import SendSMS
from app.service.notification.processor.send_telegram import SendTelegram
from core.db.model.notification import NotificationModel
from core.enum.notification_type import NotificationType
from core.domain.notification import Notification
from core.decorators.transactional import async_transactional

from uuid6 import UUID

logger = logger.get_logger(__name__)

class SendProcessor:

    def __init__(self,
        service: AsyncNotificationService,
        send_email: SendEmail,
        send_sms: SendSMS,
        send_telegram: SendTelegram,
    ):
        self._service = service
        self._send_email = send_email
        self._send_sms = send_sms
        self._send_telegram = send_telegram

    @async_transactional
    async def process(self, session, notification_id: UUID):
        notification: Notification = await self._service.get_notification_by_id(notification_id)

        handler = await self.get_handler(notification)
        await handler.push(notification)

        await self._service.update(notification)

    async def get_handler(self, notification: Notification):
        if notification.type == NotificationType.EMAIL:
            return self._send_email
        elif notification.type == NotificationType.SMS:
            return self._send_sms
        elif notification.type == NotificationType.TELEGRAM:
            return self._send_telegram