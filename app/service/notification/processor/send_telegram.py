from core.domain.notification import Notification

class SendTelegram:
    async def push(self, notification: Notification):
        notification.mark_as_sent()