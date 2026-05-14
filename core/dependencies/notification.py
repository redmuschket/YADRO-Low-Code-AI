from sqlalchemy.orm import Session
from app.service.notification.sync_notification import SyncNotificationService
from app.service.notification.sync_repository import SyncNotificationRepository


def get_notification_repo(db_session: Session) -> SyncNotificationRepository:
    """Creates a notification repository linked to the session."""
    return SyncNotificationRepository(db_session)


def get_notification_service(db_session: Session) -> NotificationService:
    """Creates a notification service by implementing a repository."""
    return NotificationService(repository=get_notification_repo(db_session))