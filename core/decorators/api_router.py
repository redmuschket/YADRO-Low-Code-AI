from functools import wraps
from flask import jsonify
from core import logger
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import ProgrammingError
from core.exception import *

logger = logger.get_logger(__name__)


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
            clean_errors = []
            for error in e.errors():
                clean_error = {
                    "type": error.get("type"),
                    "loc": error.get("loc"),
                    "msg": error.get("msg"),
                    "input": error.get("input")
                }
                clean_errors.append(clean_error)
            return jsonify({
                "error": "Invalid request data",
                "details": clean_errors
            }), 422
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
        except ProgrammingError as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            return jsonify({"error": "Database error"}), 500
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