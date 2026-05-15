from app.http.request_model.notification import NotificationCreateRequest
from app.http.response_model.notification import NotificationResponse
from core.db.model.notification import NotificationModel
from core.domain.notification import Notification
from core.enum.notification_type import NotificationType
from core.enum.notification_status import NotificationStatus

class NotificationMapper:

    @staticmethod
    def from_create_request_to_model(request: NotificationCreateRequest) -> NotificationModel:
        """Pydantic create request -> SQLAlchemy model."""
        return NotificationModel(
            type=request.type,
            recipient=request.recipient,
            message=request.message,
            subject=request.subject,
        )

    @staticmethod
    def from_model_to_response(model: NotificationModel) -> NotificationResponse:
        """SQLAlchemy model -> Pydantic response."""
        return NotificationResponse(
            id=model.id,
            status=model.status,
        )

    @staticmethod
    def from_domian_to_response(domain: Notification) -> NotificationResponse:
        """Domain object -> Pydantic response."""
        return NotificationResponse(
            id=domain.id,
            status=domain.status,
        )

    @staticmethod
    def from_model_to_domain(model: NotificationModel) -> Notification:
        """SQLAlchemy model -> Domain object."""
        return Notification(
            id=model.id,
            type=NotificationType(model.type),
            recipient=model.recipient,
            message=model.message,
            subject=model.subject,
            status=NotificationStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def from_domain_to_model(domain: Notification) -> NotificationModel:
        """Domain object -> SQLAlchemy model."""
        return NotificationModel(
            id=domain.id,
            type=domain.type,
            recipient=domain.recipient,
            message=domain.message,
            subject=domain.subject,
            status=domain.status,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )