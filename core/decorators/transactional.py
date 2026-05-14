from functools import wraps
from flask import g, jsonify
from core import logger
from core.exception import *

logger = logger.getLogger(__name__)

def transactional(func):
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