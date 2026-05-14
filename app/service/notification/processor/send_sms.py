from core.domain.notification import Notification

class SendSMSProcessor:
    async def push(self, notification: Notification):
        notification.mark_as_sent()