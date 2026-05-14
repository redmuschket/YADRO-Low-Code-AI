from core.domain.notification import Notification

class SendEmailProcessor:
    async def push(self, notification: Notification):
        notification.mark_as_sent()