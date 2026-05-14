import time
from core import logger
from functools import wraps

logger = logger.get_logger(__name__)


def timed(func):
    """
    Decorator that logs the execution time of a route.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} executed in {elapsed:.4f}s")
        return result
    return wrapper