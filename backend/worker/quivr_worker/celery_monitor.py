import asyncio
import os
import threading
from enum import Enum
from queue import Queue
from uuid import UUID

from attr import dataclass
from celery.result import AsyncResult
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger, setup_logger
from quivr_api.models.settings import settings
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.dto.inputs import NotificationUpdatableProperties
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_core.models import KnowledgeStatus
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

async_engine = create_async_engine(
    settings.pg_database_async_url,
    connect_args={"server_settings": {"application_name": "quivr-monitor"}},
    echo=True if os.getenv("ORM_DEBUG") else False,
    future=True,
    pool_pre_ping=True,
    max_overflow=0,
    pool_size=5,  # NOTE: no bouncer for now, if 6 process workers => 6
    pool_recycle=1800,
    isolation_level="AUTOCOMMIT",
)

setup_logger("notifier.log", send_log_server=False)
logger = get_logger("notifier_service")
notification_service = NotificationService()
queue = Queue()


class TaskStatus(str, Enum):
    FAILED = "task-failed"
    SUCCESS = "task-succeeded"


class TaskIdentifier(str, Enum):
    PROCESS_FILE_TASK = "process_file_task"
    PROCESS_CRAWL_TASK = "process_crawl_task"
    PROCESS_ASSISTANT_TASK = "process_assistant_task"


@dataclass
class TaskEvent:
    task_id: str
    task_name: TaskIdentifier
    notification_id: str
    knowledge_id: UUID | None
    status: TaskStatus


async def handle_error_task(
    task: TaskEvent,
    knowledge_service: KnowledgeService,
    notification_service: NotificationService,
):
    logger.error(
        f"task {task.task_id} process_file_task. Sending notifition {task.notification_id}"
    )
    notification_service.update_notification_by_id(
        task.notification_id,
        NotificationUpdatableProperties(
            status=NotificationsStatusEnum.ERROR,
            description=("An error occurred while processing the file"),
        ),
    )
    logger.error(
        f"task {task.task_id} process_file_task  failed. Updating knowledge {task.knowledge_id} to Error"
    )
    if task.knowledge_id:
        await knowledge_service.update_status_knowledge(
            task.knowledge_id, KnowledgeStatus.ERROR
        )
    logger.error(
        f"task {task.task_id} process_file_task . Updating knowledge {task.knowledge_id} status to Error"
    )


async def handle_success_task(
    task: TaskEvent,
    knowledge_service: KnowledgeService,
    notification_service: NotificationService,
):
    logger.info(
        f"task {task.task_id} process_file_task succeeded. Sending notification {task.notification_id}"
    )
    notification_service.update_notification_by_id(
        task.notification_id,
        NotificationUpdatableProperties(
            status=NotificationsStatusEnum.SUCCESS,
            description=(
                "Your file has been properly uploaded!"
                if task.task_name == TaskIdentifier.PROCESS_FILE_TASK
                else "Your URL has been properly crawled!"
            ),
        ),
    )
    if task.knowledge_id:
        await knowledge_service.update_status_knowledge(
            knowledge_id=task.knowledge_id,
            status=KnowledgeStatus.UPLOADED,
        )
    logger.info(
        f"task {task.task_id} process_file_task failed. Updating knowledge {task.knowledge_id} to UPLOADED"
    )


async def handler_loop():
    async with AsyncSession(
        async_engine, expire_on_commit=False, autoflush=False
    ) as session:
        await session.execute(
            text("SET SESSION idle_in_transaction_session_timeout = '1min';")
        )
        knowledge_service = KnowledgeService(KnowledgeRepository(session))
        notification_service = NotificationService()
        logger.info("Initialized knowledge_service. Listening to task event...")
        while True:
            try:
                event: TaskEvent = queue.get()
                if event.status == TaskStatus.FAILED:
                    await handle_success_task(
                        task=event,
                        knowledge_service=knowledge_service,
                        notification_service=notification_service,
                    )

                if event.status == TaskStatus.SUCCESS:
                    await handle_error_task(
                        task=event,
                        knowledge_service=knowledge_service,
                        notification_service=notification_service,
                    )

            except Exception as e:
                logger.error(f"Excpetion occured handling event {event}: {e}")


def notifier(app):
    state = app.events.State()

    def handle_task_event(event):
        try:
            state.event(event)
            task = state.tasks.get(event["uuid"])
            task_result = AsyncResult(task.id, app=app)
            task_name, task_kwargs = task_result.name, task_result.kwargs

            if task_name == TaskIdentifier.PROCESS_FILE_TASK:
                logger.debug(f"Received Event : {task} - {task_name} {task_kwargs} ")
                knowledge_id = task_kwargs.get("knowledge_id", None)
                notification_id = task_kwargs.get("notification_id", None)
                event = TaskEvent(
                    task_id=task,
                    task_name=TaskIdentifier(task_name),
                    knowledge_id=knowledge_id,
                    notification_id=notification_id,
                    status=TaskStatus(event["type"]),
                )
                queue.put(event)
            elif task_name == "process_assistant_task":
                logger.debug(f"Received Event : {task} - {task_name} {task_kwargs} ")
                task_id = task_kwargs["task_id"]
                event = TaskEvent(
                    task_id=task,
                    task_name=TaskIdentifier(task_name),
                    knowledge_id=None,
                    notification_id=task_id,
                    status=TaskStatus(event["type"]),
                )
                queue.put(event)

        except Exception as e:
            logger.exception(f"handling event {event} raised exception: {e}")

    with app.connection() as connection:
        recv = app.events.Receiver(
            connection,
            handlers={
                "task-failed": handle_task_event,
                "task-succeeded": handle_task_event,
            },
        )
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == "__main__":
    logger.info("Started  quivr-notifier service...")

    def start_handler():
        asyncio.run(handler_loop())

    thread = threading.Thread(target=start_handler, daemon=True)
    thread.start()

    notifier(celery)
