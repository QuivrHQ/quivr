# celery_config.py
import os

from celery import Celery

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")
CELERY_BROKER_QUEUE_NAME = os.getenv("CELERY_BROKER_QUEUE_NAME", "quivr")

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
elif CELERY_BROKER_URL.startswith("redis"):
    celery = Celery(
        __name__,
        broker=CELERY_BROKER_URL,
        backend=CELERY_BROKER_URL,
        task_concurrency=4,
        worker_prefetch_multiplier=1,
        task_serializer="json",
    )
else:
    raise ValueError(f"Unsupported broker URL: {CELERY_BROKER_URL}")
