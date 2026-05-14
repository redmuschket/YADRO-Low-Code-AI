from functools import wraps
from flask import g, jsonify
from core import logger
from core.exception import *

logger = logger.get_logger(__name__)

def sync_transactional(func):
    """
    A decorator for routes that need a transaction.
    On success, it automatically commits sessions from g.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if hasattr(g, 'db_session') and g.db_session:
                g.db_session.commit()
                logger.debug("The transaction has been successfully committed")
            return result
        except Exception as e:
            if hasattr(g, 'db_session') and g.db_session:
                g.db_session.rollback()
                logger.error(f"Error, the transaction was canceled: {e}")
            raise TransactionError(e)
    return wrapper


def async_transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.pop('session', None)
        if session is None:
            raise ValueError("Session is required")
        try:
            result = await func(session=session, *args, **kwargs)
            await session.commit()
            return result
        except Exception:
            await session.rollback()
            raise
    return wrapper