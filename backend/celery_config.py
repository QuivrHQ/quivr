# celery_config.py
import os

from celery import Celery
from logger import get_logger

logger = get_logger(__name__)

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")
CELERY_BROKER_QUEUE_NAME = os.getenv("CELERY_BROKER_QUEUE_NAME", "quivr")
REDIS_HOST = os.getenv("REDIS_HOST", "")
REDIS_PORT = os.getenv("REDIS_PORT", "")
REDIS_PASS = os.getenv("REDIS_PASS", "")

celery = Celery(__name__)

if CELERY_BROKER_URL.startswith("sqs"):
    broker_transport_options = {
        CELERY_BROKER_QUEUE_NAME: {
            "my-q": {
                "url": CELERY_BROKER_URL,
            }
        }
    }
    celery = Celery(
        __name__,
        broker=CELERY_BROKER_URL,
        task_serializer="json",
        task_concurrency=4,
        worker_prefetch_multiplier=1,
        broker_transport_options=broker_transport_options,
    )
    celery.conf.task_default_queue = CELERY_BROKER_QUEUE_NAME
elif REDIS_HOST:
    logger.info(f"Using Redis as broker: {REDIS_HOST}:{REDIS_PORT}")
    celery = Celery(
        __name__,
        # redis://:password@hostname:port/db_number
        broker=f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0",
        backend=f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0",
        result_backend=f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0",
        task_concurrency=4,
        worker_prefetch_multiplier=1,
        task_serializer="json",
    )
else:
    raise ValueError(f"Unsupported broker URL: {CELERY_BROKER_URL}")
