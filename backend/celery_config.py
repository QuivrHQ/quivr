# celery_config.py
import os

import dotenv
from celery import Celery

dotenv.load_dotenv()

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
        broker=f"{CELERY_BROKER_URL}",
        backend=f"{CELERY_BROKER_URL}",
        task_concurrency=4,
        worker_prefetch_multiplier=2,
        task_serializer="json",
    )

    # Configure Redis priority queues
    celery.conf.broker_transport_options = {
        "queue_order_strategy": "priority",
        "priority_steps": list(range(10)),  # 0-9 priority levels
        "sep": ":",
    }

    # Define task routes for priorities
    celery.conf.task_routes = {
        "process_file_and_notify": {
            "queue": "celery",
            "priority": 9,
        },  # Highest priority
        "process_crawl_and_notify": {"queue": "celery", "priority": 8},
        "*": {"queue": "celery", "priority": 5},  # Default priority for other tasks
    }
else:
    raise ValueError(f"Unsupported broker URL: {CELERY_BROKER_URL}")


celery.autodiscover_tasks(["modules.sync", "modules", "middlewares", "packages"])
