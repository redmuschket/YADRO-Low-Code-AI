from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional
import re

from core.enum.notification_type import NotificationType


class NotificationCreateRequest(BaseModel):
    """The scheme for creating a notification."""
    type: NotificationType
    recipient: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=5000)
    subject: Optional[dict] = Field(default=None)

    @field_validator('recipient')
    @classmethod
    def validate_recipient(cls, v: str, info: ValidationInfo) -> str:
        ntype = info.data.get('type')
        if ntype is None:
            return v

        if ntype == NotificationType.EMAIL:
            # Simple email verification: something@something.something
            if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', v):
                raise ValueError('Incorrect email')
        elif ntype == NotificationType.SMS:
            # Phone number: + and digits, length 10-15
            if not re.match(r'^\+?[1-9]\d{1,14}$', v):
                raise ValueError('Incorrect phone number')
        elif ntype == NotificationType.TELEGRAM:
            # Telegram username: @ и 5-32 characters (letters, numbers, _)
            if not re.match(r'^@[A-Za-z0-9_]{5,32}$', v):
                raise ValueError('Incorrect Telegram username (must start with @, 5-32 characters)')
        return v