from app.service.notification.async_repository import AsyncNotificationRepository
from core.db.model.notification import NotificationModel
from core.enum.notification_status import NotificationStatus
from app.http.request_model.notification import NotificationCreateRequest
from core.data_mapper.notification import NotificationMapper
from app.http.response_model.notification import NotificationResponse
from core.domain.notification import Notification
from core.exception import *

from typing import Optional
from uuid6 import UUID


class AsyncNotificationService:

    def __init__(self, repository: AsyncNotificationRepository):
        self.repository = repository

    async def get_notification_by_id(self, uuid_notification: UUID) -> Notification:
        """Get a notification by uuid."""
        notification_model: Optional[NotificationModel] = await self.repository.get_by_id(uuid_notification)
        if notification_model is None:
            raise NotificationGetError(f"There are no values for id in the database: {uuid_notification}")
        return NotificationMapper.from_model_to_domain(notification_model)

    async def update(self, notification: Notification):
        """Update a notification."""
        notification_model = NotificationMapper.from_domain_to_model(notification)
        await self.repository.update(notification_model)