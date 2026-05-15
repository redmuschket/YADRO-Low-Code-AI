import pytest
from unittest.mock import Mock, patch
from uuid6 import uuid7
from uuid import UUID
from app.service.notification.sync_notification import SyncNotificationService
from app.service.notification.sync_repository import SyncNotificationRepository
from core.db.model.notification import NotificationModel
from core.enum.notification_type import NotificationType
from core.enum.notification_status import NotificationStatus
from core.exception.notification import NotificationGetError


class TestNotificationService:

    @pytest.fixture
    def mock_repo(self):
        return Mock(spec=SyncNotificationRepository)

    @pytest.fixture
    def service(self, mock_repo):
        return SyncNotificationService(repository=mock_repo)

    def test_create_notification(self, service, mock_repo, notification_data):
        """Checking the creation of the notification."""
        from app.http.request_model.notification import NotificationCreateRequest

        request = NotificationCreateRequest(**notification_data)

        saved_model = NotificationModel(
            id=uuid7(),
            type=NotificationType.EMAIL,
            recipient=request.recipient,
            message=request.message,
            status=NotificationStatus.PENDING
        )
        mock_repo.save.return_value = saved_model

        response = service.create_notification_by_request(request)

        mock_repo.save.assert_called_once()
        assert response.id == saved_model.id
        assert response.status == NotificationStatus.PENDING

    def test_get_notification_found(self, service, mock_repo):
        """Checking the receipt of an existing notification."""
        notification_id = UUID('00000000-0000-0000-0000-000000000001')
        model = NotificationModel(
            id=notification_id,
            type=NotificationType.EMAIL,
            recipient="user@example.com",
            message="Test",
            status=NotificationStatus.SENT
        )
        mock_repo.get_by_id.return_value = model

        result = service.get_notification_by_id(notification_id)

        assert result.id == model.id
        assert result.status == NotificationStatus.SENT

    def test_get_notification_not_found(self, service, mock_repo, db_session):
        """Verification of receipt of a non-existent notification."""
        mock_repo.get_by_id.return_value = None

        with pytest.raises(NotificationGetError):
            service.get_notification_by_id(UUID('00000000-0000-0000-0000-000000000001'))