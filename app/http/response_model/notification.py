from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional
import re
from uuid import UUID

from core import config
from core.enum.notification_status import NotificationStatus


class NotificationResponse(BaseModel):
    """The scheme for creating a notification."""
    status: NotificationStatus = Field(
        ...,
        description=f"Notification status. Available values: {', '.join([s.value for s in NotificationStatus])}"
    )
    id: Optional[UUID] = Field(
        default=None,
        description=f"UUID version {config.NOTIFICATION_UUID_VERSION} identifier"
    )

    @field_validator('id', mode='after')
    @classmethod
    def check_version(cls, v: Optional[UUID]) -> Optional[UUID]:
        """Validate that UUID matches the required version from config.

        Args:
            v: UUID instance or None

        Returns:
            Validated UUID or None

        Raises:
            ValueError: If UUID version doesn't match config value
        """
        if v is not None and v.version != config.NOTIFICATION_UUID_VERSION:
            raise ValueError(
                f'Only UUID version {config.NOTIFICATION_UUID_VERSION} is allowed, '
                f'got version {v.version}'
            )
        return v
