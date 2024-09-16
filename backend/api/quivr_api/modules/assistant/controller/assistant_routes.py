from typing import Annotated, List
from uuid import uuid4
import io
from fastapi import APIRouter, Depends, Request, UploadFile, HTTPException

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth.auth_bearer import AuthBearer, get_current_user
from quivr_api.modules.assistant.services.tasks_service import TasksService
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.assistant.entity.assistant_entity import (
    Assistant,
    AssistantInput,
    AssistantSettings,
    AssistantInputOutput
)
from quivr_api.modules.assistant.dto.inputs import CreateTask
from quivr_api.modules.user.entity.user_identity import UserIdentity
from quivr_api.modules.notification.service.notification_service import NotificationService
from quivr_api.modules.notification.dto.inputs import (
    CreateNotification,
    NotificationUpdatableProperties,
)
from quivr_api.modules.upload.service.upload_file import (
    upload_file_storage,
)
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum



logger = get_logger(__name__)
logger = get_logger(__name__)


assistant_router = APIRouter()

notification_service = NotificationService()


TasksServiceDep = Annotated[TasksService, Depends(get_service(TasksService))]
UserIdentityDep = Annotated[UserIdentity, Depends(get_current_user)]

assistant1 = Assistant(
        id=1,
        name="Assistant 1",
        description="Assistant 1 description",
        file1_name="Fichier 1",
        file2_name="Fichier 2",
        settings=AssistantSettings(
            inputs=[
                AssistantInput(
                    name="Complex File",
                    description="Complex File to read",
                    type="boolean",
            )
        ]
    ),
)

assistants=[assistant1]

@assistant_router.get(
    "/assistants", dependencies=[Depends(AuthBearer())], tags=["Assistant"]
)
async def get_assistants(
    request: Request,
    current_user: UserIdentity = Depends(get_current_user),
) -> List[Assistant]:
    logger.info("Getting assistants")
    
    return assistants


@assistant_router.get(
    "/assistants/tasks", dependencies=[Depends(AuthBearer())], tags=["Assistant"]
)
async def get_tasks(
    request: Request,
    current_user: UserIdentityDep,
    tasks_service: TasksServiceDep,
):
    logger.info("Getting tasks")
    return await tasks_service.get_tasks_by_user_id(current_user.id)


@assistant_router.post(
    "/assistants/task", dependencies=[Depends(AuthBearer())], tags=["Assistant"]
)
async def create_task(
    request: Request,
    file1: UploadFile,
    file2: UploadFile,
    assistant_id: int,
    current_user: UserIdentityDep,
    tasks_service: TasksServiceDep,
    assistant_settings: List[AssistantInputOutput] | None = None,

):
    
    assistant = next((assistant for assistant in assistants if assistant.id == assistant_id), None)
    if assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    
    notification_uuid = uuid4()
    upload_notification = notification_service.add_notification(
        CreateNotification(
            user_id=current_user.id,
            bulk_id=notification_uuid,
            status=NotificationsStatusEnum.INFO,
            title=f"{assistant.name}",
            category="assistant",
        )
    )
    
    file1_name_path= str(assistant_id)+ "/" + str(notification_uuid) + "/" + str(file1.filename)
    file2_name_path= str(assistant_id) + "/" + str(notification_uuid) + "/" + str(file2.filename)
    
    buff_reader1 = io.BufferedReader(file1.file)  # type: ignore
    buff_reader2 = io.BufferedReader(file2.file)  # type: ignore
    
    try:
        await upload_file_storage(buff_reader1, file1_name_path)
        await upload_file_storage(buff_reader2, file2_name_path)
    except Exception as e:
        logger.exception(f"Exception in upload_route {e}")
        notification_service.update_notification_by_id(
            upload_notification.id if upload_notification else None,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.ERROR,
                description="There was an error uploading the file",
            ),
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to upload file to storage. {e}"
        )
    
    task = CreateTask(
        pretty_id=str(notification_uuid)
    )
    
    return await tasks_service.create_task(task, current_user.id)


@assistant_router.get(
    "/assistants/task/{task_id}",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
)
async def get_task(
    request: Request,
    task_id: str,
    current_user: UserIdentityDep,
    tasks_service: TasksServiceDep,
):
    logger.info("Getting task")
    return {"message": "Hello World"}


@assistant_router.delete(
    "/assistants/task/{task_id}",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
)
async def delete_task(
    request: Request,
    task_id: int,
    current_user: UserIdentityDep,
    tasks_service: TasksServiceDep,
):
    return await tasks_service.delete_task(task_id, current_user.id)
