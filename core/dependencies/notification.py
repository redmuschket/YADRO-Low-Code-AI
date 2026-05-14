from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.notification.sync_notification import SyncNotificationService
from app.service.notification.sync_repository import SyncNotificationRepository
from app.service.notification.async_repository import AsyncNotificationRepository
from app.service.notification.async_notification import AsyncNotificationService


def get_sync_notification_repository(db_session: Session) -> SyncNotificationRepository:
    """Creates a sync notification repository linked to the session."""
    return SyncNotificationRepository(db_session)

def get_sync_notification_service(db_session: Session) -> SyncNotificationService:
    """Creates a sync notification service by implementing a repository."""
    return SyncNotificationService(repository=get_sync_notification_repository(db_session))

def get_async_notification_repository(db_session: AsyncSession) -> AsyncNotificationRepository:
    """Creates async notification repository linked to the session."""
    return AsyncNotificationRepository(db_session)

def get_async_notification_service(db_session: AsyncSession) -> AsyncNotificationService:
    """Creates async notification service by implementing a repository."""
    return AsyncNotificationService(repository=get_async_notification_repository(db_session))