from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


def get_sync_notification_repository(db_session: Session):
    """Creates a sync notification repository linked to the session."""
    from app.service.notification.sync_repository import SyncNotificationRepository
    return SyncNotificationRepository(db_session)


def get_sync_notification_service(db_session: Session):
    """Creates a sync notification service by implementing a repository."""
    from app.service.notification.sync_notification import SyncNotificationService
    return SyncNotificationService(repository=get_sync_notification_repository(db_session))


def get_async_notification_repository(db_session: AsyncSession):
    """Creates async notification repository linked to the session."""
    from app.service.notification.async_repository import AsyncNotificationRepository
    return AsyncNotificationRepository(db_session)


def get_async_notification_service(db_session: AsyncSession):
    """Creates async notification service by implementing a repository."""
    from app.service.notification.async_notification import AsyncNotificationService
    return AsyncNotificationService(repository=get_async_notification_repository(db_session))


def get_processor_send_email():
    from app.service.notification.processor.send_email import SendEmailProcessor
    return SendEmailProcessor()


def get_processor_send_sms():
    from app.service.notification.processor.send_sms import SendSMSProcessor
    return SendSMSProcessor()


def get_processor_send_telegram():
    from app.service.notification.processor.send_telegram import SendTelegramProcessor
    return SendTelegramProcessor()


def get_processor_notification_send(db_session: AsyncSession):
    from app.service.notification.processor.send import SendProcessor
    return SendProcessor(
        send_sms=get_processor_send_sms(),
        send_email=get_processor_send_email(),
        send_telegram=get_processor_send_telegram(),
        service=get_async_notification_service(db_session),
    )