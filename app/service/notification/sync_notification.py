from app.service.notification.sync_repository import SyncNotificationRepository

class SyncNotificationService:

    def __init__(self, repository: SyncNotificationRepository):
        self.repository = repository