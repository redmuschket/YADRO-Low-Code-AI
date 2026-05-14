import enum

class NotificationType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    TELEGRAM = "telegram"