from core.exceptions import *
from core import logger

from functools import wraps
from typing import Callable, Any
from fastapi import HTTPException
from fastapi import status

logger = logger.get_logger(__name__)
AUTH_DOCSTRING = """
    ## Authentication
    - Requires JWT token in Authorization header (Bearer token)
    - The system automatically extracts user ID from the token and passes it via X-User-Id header
"""


def handle_exceptions(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        # ---- Auth / token errors (must be before generic Exception) ----
        except MissingHeaderError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Authorization header required: {str(e)}",
            )
        except InvalidSchemeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid authentication scheme: {str(e)}",
            )
        except AccessTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Access token required: {str(e)}",
            )
        except RefreshTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Refresh token required: {str(e)}",
            )
        except ValidationTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}",
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid request data: {str(e)}"
            )
        except PatentCreationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Patent creation process failed"
            )
        except PatentGetError as e:
            logger.error(f"Patent service error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patents not found or access denied"
            )
        except AnalogCreationLinkError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Analog operation failed: {str(e)}"
            )
        except ServiceRepositoryError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Storage service temporarily unavailable: {str(e)}"
            )
        except InternalServerErrorException as e:
            logger.error(f"Internal server error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    return wrapper

def auth_doc(endpoint):
    """Декоратор для добавления описания аутентификации к endpoint'ам"""
    if hasattr(endpoint, '__doc__') and endpoint.__doc__:
        endpoint.__doc__ = endpoint.__doc__.rstrip() + "\n\n" + AUTH_DOCSTRING
    else:
        endpoint.__doc__ = AUTH_DOCSTRING
    return endpoint