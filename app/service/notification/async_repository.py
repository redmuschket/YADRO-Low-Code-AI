from app.service.base_async_repository import BaseAsyncRepository
from core.db.model.notification import NotificationModel

from sqlalchemy import select
from uuid6 import UUID


class AsyncNotificationRepository(BaseAsyncRepository):

    async def update(self, notification: NotificationModel) -> NotificationModel:
        """Updates an existing notification entity."""
        merged = await self._db.merge(notification)
        await self._db.flush()
        return merged

    async def get_by_id(self, notification_id: UUID) -> NotificationModel | None:
        """Finds a notification by its UUID."""
        stmt = select(NotificationModel).where(NotificationModel.id == notification_id)
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()