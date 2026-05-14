import uuid6
from core import config


def generate_uuid_for_notification_from_config():
    """Generates UUID v{N}"""
    if config.NOTIFICATION_UUID_VERSION == 7:
        return uuid6.uuid7()
    else:
        raise NotImplementedError(f"UUID version {config.NOTIFICATION_UUID_VERSION} is not supported")