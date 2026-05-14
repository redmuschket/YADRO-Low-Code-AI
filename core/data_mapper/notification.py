from app.http.request_model.notification import NotificationCreateRequest
from app.http.response_model.notification import NotificationCreateResponse
from core.db.model.notification import NotificationModel
from core.domain.notification import Notification

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
    def from_model_to_create_response(model: NotificationModel) -> NotificationCreateResponse:
        """SQLAlchemy model -> Pydantic create response."""
        return NotificationCreateResponse(
            id=model.id,
            status=model.status,
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