from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON

from core.enum.notification_status import NotificationStatus
from core.enum.notification_type import NotificationType
from core.db.base import Base
import enum

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid7)
    type = Column(
        SAEnum(NotificationType, name='notification_type_enum', create_type=True),
        nullable=False
    )
    recipient = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    subject = Column(JSON, nullable=True)
    status = Column(
        SAEnum(NotificationStatus, name='notification_status_enum', create_type=True),
        default=NotificationStatus.PENDING,
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())