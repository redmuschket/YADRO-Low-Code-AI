from app.service.notification.sync_repository import SyncNotificationRepository
from core.db.model.notification import NotificationModel
from core.enum.notification_status import NotificationStatus
from app.http.request_model.notification import NotificationCreateRequest
from core.data_mapper.notification import NotificationMapper
from app.http.response_model.notification import NotificationResponse
from core.domain.notification import Notification
from core.exception import *

from uuid6 import UUID


class SyncNotificationService:

    def __init__(self, repository: SyncNotificationRepository):
        self.repository = repository

    def create_notification_by_request(
        self,
        request:NotificationCreateRequest
    ) -> NotificationResponse:
        """Creates a notification by request."""
        notification: NotificationModel = NotificationMapper.from_create_request_to_model(request)
        notification: NotificationModel = self.repository.save(notification)
        return NotificationMapper.from_model_to_response(notification)

    def get_notification_by_id(self, uuid_notification: UUID) -> Notification:
        """Get a notification by uuid."""
        notification_model: Optional[NotificationModel] = self.repository.get_by_id(uuid_notification)
        if notification_model is None:
            raise NotificationGetError(f"There are no values for id in the database: {uuid_notification}")
        return NotificationMapper.from_model_to_domain(notification_model)