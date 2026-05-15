import pytest
from unittest.mock import patch, Mock
from uuid import UUID
from core.enum.notification_status import NotificationStatus


class TestNotificationAPI:
    """Tests for API endpoints."""

    @patch('app.http.controllers.notification.send_notification_task')
    def test_create_notification_success(self, mock_task, client, notification_data, db_session):
        """Checking the successful creation of the notification."""
        mock_task.delay = Mock()

        response = client.post(
            '/api/v1/notifications/',
            json=notification_data,
            content_type='application/json'
        )

        assert response.status_code == 202
        data = response.get_json()
        assert 'id' in data
        assert data['status'] == 'queued'
        mock_task.delay.assert_called_once()

    def test_create_notification_invalid_email(self, client):
        """Email validation check."""
        response = client.post(
            '/api/v1/notifications/',
            json={
                "type": "email",
                "recipient": "invalid-email",
                "message": "Test"
            },
            content_type='application/json'
        )

        assert response.status_code == 422
        data = response.get_json()
        assert 'error' in data
        assert 'details' in data

    def test_create_notification_invalid_phone(self, client):
        """Phone validation check."""
        response = client.post(
            '/api/v1/notifications/',
            json={
                "type": "sms",
                "recipient": "not-a-phone",
                "message": "Test"
            },
            content_type='application/json'
        )

        assert response.status_code == 422

    def test_create_notification_invalid_telegram(self, client):
        """Checking the Telegram username validation."""
        response = client.post(
            '/api/v1/notifications/',
            json={
                "type": "telegram",
                "recipient": "without_at",
                "message": "Test"
            },
            content_type='application/json'
        )

        assert response.status_code == 422

    @patch('app.http.controllers.notification.send_notification_task')
    def test_get_notification_success(self, mock_task, client, db_session):
        """Verification of notification receipt."""
        from core.db.model.notification import NotificationModel
        from core.enum.notification_type import NotificationType
        from core.enum.notification_status import NotificationStatus

        notification = NotificationModel(
            type=NotificationType.EMAIL,
            recipient="user@example.com",
            message="Test message",
            status=NotificationStatus.SENT
        )
        db_session.add(notification)
        db_session.commit()

        response = client.get(f'/api/v1/notifications/{notification.id}')

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == str(notification.id)
        assert data['status'] == 'sent'

    def test_get_notification_not_found(self, client, db_session):
        """Checking a 404 for a non-existent notification."""
        response = client.get(f'/api/v1/notifications/00000000-0000-0000-0000-000000000000')

        assert response.status_code == 404