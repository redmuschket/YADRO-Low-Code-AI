from functools import wraps
from flask import jsonify
import logging
from pydantic import ValidationError as PydanticValidationError
from core.exceptions import *

logger = logging.getLogger(__name__)


def handle_exceptions(func):
    """
    Decorator for Flask routes.
    Catches known exceptions and returns JSON with appropriate HTTP status.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PydanticValidationError as e:
            logger.warning(f"Validation error in {func.__name__}: {e.errors()}")
            return jsonify({"error": "Invalid request data", "details": e.errors()}), 422
        except ValidationError as e:
            logger.warning(f"Business validation failed in {func.__name__}: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except NotificationGetError as e:
            logger.warning(f"Notification not found in {func.__name__}: {str(e)}")
            return jsonify({"error": str(e)}), 404
        except NotificationCreationError as e:
            logger.error(f"Notification creation failed in {func.__name__}: {str(e)}")
            return jsonify({"error": str(e)}), 500
        except NotificationServiceError as e:
            logger.error(f"Notification service error in {func.__name__}: {str(e)}")
            return jsonify({"error": str("Service temporarily unavailable")}), 503
        except TransactionError as e:
            logger.error(f"Transaction error in {func.__name__}: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
        except ServiceRepositoryError as e:
            logger.critical(f"Repository error in {func.__name__}: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    return wrapper