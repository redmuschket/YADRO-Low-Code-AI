import os
import logging
from celery import Celery
from celery.signals import after_setup_logger
from dotenv import load_dotenv

load_dotenv()

app = Celery(
    'notifications',
    broker=os.getenv('CELERY_BROKER_URL', 'amqp://admin:admin1admin@localhost:5672'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'rpc://'),
    include=['workers.tasks.notifications']
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_hijack_root_logger=False,
)


@after_setup_logger.connect
def setup_celery_logger(logger, **kwargs):
    """
    Sending error is setting up the Celery logger.
    """
    from core import logger as app_logger
    celery_logger = app_logger.get_logger('celery')

    # Copying handlers from our logger to Celery
    for handler in celery_logger.handlers:
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
