from .service import ServiceError

class NotificationServiceError(ServiceError):
    """Notification service level error"""
    pass

class NotificationCreationError(NotificationServiceError):
    """Notification creation error"""
    pass

class NotificationGetError(NotificationServiceError):
    """Receiving error"""
    pass