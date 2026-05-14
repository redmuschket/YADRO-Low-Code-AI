from app.service.notification.sync_repository import SyncNotificationRepository
from core.db.model.notification import NotificationModel
from core.enum.notification_status import NotificationStatus
from app.http.request_model.notification import NotificationCreateRequest
from core.data_mapper.notification import NotificationMapper
from app.http.response_model.notification import NotificationCreateResponse

class SyncNotificationService:

    def __init__(self, repository: SyncNotificationRepository):
        self.repository = repository

    def create_notification_by_request(
        self,
        request:NotificationCreateRequest
    ) -> NotificationCreateResponse:
        """Creates a notification by request."""
        notification: NotificationModel = NotificationMapper.from_create_request_to_model(request)
        notification: NotificationModel = self.repository.save(notification)
        return NotificationMapper.from_model_to_create_response(notification)