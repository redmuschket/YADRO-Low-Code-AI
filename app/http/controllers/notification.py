from typing import Optional
from uuid import UUID
from flask import jsonify
from flask import request, g

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
        from workers.tasks.notifications import send_notification_task
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

        notification.status = NotificationStatus.QUEUED

        send_notification_task.delay(str(notification.id))

        logger_user.info(f"Notification {notification.id} queued for sending")

        return jsonify(notification.model_dump()), HTTP_202_ACCEPTED