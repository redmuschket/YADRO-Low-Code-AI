from fastapi import Depends, HTTPException, status
from typing import Optional
from uuid import UUID

from app.service.notification.sync_notification import SyncNotificationService
from app.http.request_model.notification import NotificationCreateRequest
from app.http.response_model.notification import NotificationCreateResponse
from core.enum.notification_status import NotificationStatus
from core.http_status import HttpStatus, HTTP_202_ACCEPTED
from core import logger

logger_user = logger.get_logger('user')
logger_system = logger.get_logger(__name__)


class NotificationController:
    """Handles HTTP requests and orchestrates service calls."""

    def create_notification(self) -> tuple[NotificationCreateResponse, HttpStatus]:
        """
        Process notification creation request.

        Steps:
        1. Validate request (already done by Pydantic)
        2. Call service to create notification
        4. Send it to Celery
        3. Return response with notification ID
        """
        data = NotificationCreateRequest(**request.json)

        service: SyncNotificationService = g.notification_service
        notification: NotificationCreateResponse = service.create_notification_by_request(request=data)

        send_notification_task.delay(str(notification.id))
        logger_user.info(f"Notification {notification.id} queued for sending")

        return notification, HTTP_202_ACCEPTED

    async def get_notification_status(
            self,
            notification_id: UUID
    ) -> Optional[NotificationStatusResponse]:
        """Get notification status by ID."""
        result = await self.service.get_notification_status(notification_id)
        if result:
            return NotificationStatusResponse(
                id=notification_id,
                status=result["status"],
                created_at=result["created_at"],
                sent_at=result.get("sent_at")
            )
        return None