from app.service.base_sync_repository import BaseSyncRepository
from core.db.model.notification import NotificationModel

class SyncNotificationRepository(BaseSyncRepository):

    def save(self, notification:NotificationModel):
        return self._save_entity(notification)