from app.http.request_model.notification import NotificationCreateRequest
from app.http.response_model.notification import NotificationCreateResponse
from core.db.model.notification import NotificationModel

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