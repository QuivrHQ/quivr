# celery_config.py
import os

import dotenv
from celery import Celery

dotenv.load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")
CELERY_BROKER_QUEUE_NAME = os.getenv("CELERY_BROKER_QUEUE_NAME", "quivr")

celery = Celery(__name__)

if CELERY_BROKER_URL.startswith("redis"):
    celery = Celery(
        __name__,
        broker=f"{CELERY_BROKER_URL}",
        backend=f"{CELERY_BROKER_URL}",
        task_concurrency=4,
        worker_prefetch_multiplier=2,
        task_serializer="json",
        result_extended=True,
        task_send_sent_event=True,
    )
else:
    raise ValueError(f"Unsupported broker URL: {CELERY_BROKER_URL}")

celery.autodiscover_tasks(["quivr_api.modules.chat"])
