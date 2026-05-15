from app.service.base_sync_repository import BaseSyncRepository
from core.db.model.notification import NotificationModel

from sqlalchemy import select
from uuid6 import UUID


class SyncNotificationRepository(BaseSyncRepository):

    def save(self, notification:NotificationModel):
        return self._save_entity(notification)

    def get_by_id(self, notification_id: UUID) -> NotificationModel | None:
        """Finds a notification by its UUID."""
        stmt = select(NotificationModel).where(NotificationModel.id == notification_id)
        result = self._db.execute(stmt)
        return result.scalar_one_or_none()