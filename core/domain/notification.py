from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import re

from core.enum.notification_type import NotificationType
from core.enum.notification_status import NotificationStatus


@dataclass
class Notification:

    type: NotificationType
    recipient: str
    message: str
    id: Optional[UUID] = None
    subject: Optional[dict] = None
    status: NotificationStatus = NotificationStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Валидация после инициализации."""
        if not self.message or not self.message.strip():
            raise ValueError("The notification message cannot be empty")

        if not self.recipient or not self.recipient.strip():
            raise ValueError("The recipient cannot be empty")

        self._validate_recipient_by_type()

    def _validate_recipient_by_type(self) -> None:
        """Checks the recipient's format depending on the type of notification.."""
        if self.type == NotificationType.EMAIL:
            if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', self.recipient):
                raise ValueError(f"Incorrect email: {self.recipient}")
        elif self.type == NotificationType.SMS:
            if not re.match(r'^\+?[1-9]\d{1,14}$', self.recipient):
                raise ValueError(f"Incorrect phone number: {self.recipient}")
        elif self.type == NotificationType.TELEGRAM:
            if not re.match(r'^@[A-Za-z0-9_]{5,32}$', self.recipient):
                raise ValueError(f"Incorrect Telegram username: {self.recipient}")

    def can_be_sent(self) -> bool:
        """Checks if the notification can be sent."""
        return self.status in (NotificationStatus.PENDING, NotificationStatus.QUEUED)

    def can_be_cancelled(self) -> bool:
        """Checks if the notification can be cancelled."""
        return self.status in (NotificationStatus.PENDING, NotificationStatus.QUEUED)

    def mark_as_sent(self) -> None:
        """Marks the notification as sent."""
        if not self.can_be_sent():
            raise ValueError(f"Cannot mark as sent: current status is {self.status.value}")
        self.status = NotificationStatus.SENT

    def mark_as_failed(self) -> None:
        """Marks the notification as failed."""
        self.status = NotificationStatus.FAILED