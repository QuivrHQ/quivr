import io
from typing import Annotated, List
from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth.auth_bearer import AuthBearer, get_current_user
from quivr_api.modules.assistant.dto.inputs import CreateTask
from quivr_api.modules.assistant.entity.assistant_entity import (
    Assistant,
    AssistantInput,
    AssistantSettings,
)
from quivr_api.modules.assistant.services.tasks_service import TasksService
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.upload.service.upload_file import (
    upload_file_storage,
)
from quivr_api.modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)
logger = get_logger(__name__)


assistant_router = APIRouter()


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

assistants = [assistant1]


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
    assistant_settings: str = Form(None),
):
    assistant = next(
        (assistant for assistant in assistants if assistant.id == assistant_id), None
    )
    if assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")

    notification_uuid = uuid4()

    file1_name_path = f"{assistant_id}/{notification_uuid}/{file1.filename}"
    file2_name_path = f"{assistant_id}/{notification_uuid}/{file2.filename}"

    buff_reader1 = io.BufferedReader(file1.file)  # type: ignore
    buff_reader2 = io.BufferedReader(file2.file)  # type: ignore

    try:
        await upload_file_storage(buff_reader1, file1_name_path)
        await upload_file_storage(buff_reader2, file2_name_path)
    except Exception as e:
        logger.exception(f"Exception in upload_route {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to upload file to storage. {e}"
        )

    # Parse the assistant_settings string into a list of dictionaries
    import json

    if assistant_settings is not None:
        assistant_settings_list = json.loads(assistant_settings)
        logger.info(f"Assistant settings: {assistant_settings_list}")
    else:
        assistant_settings_list = []

    # Convert the list of dictionaries to a single dictionary
    assistant_settings_dict = {
        item["name"]: item["value"] for item in assistant_settings_list
    }

    logger.error(f"Assistant settings: {assistant_settings_dict}")
    task = CreateTask(
        assistant_id=assistant_id,
        pretty_id=str(notification_uuid),
        settings=assistant_settings_dict,
    )

    task_created = await tasks_service.create_task(task, current_user.id)

    celery.send_task(
        "process_assistant_task",
        kwargs={
            "assistant_id": assistant_id,
            "notification_uuid": notification_uuid,
            "file1_name_path": file1_name_path,
            "file2_name_path": file2_name_path,
            "task_id": task_created.id,
            "user_id": str(current_user.id),
        },
    )
    return task_created


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
    return await tasks_service.get_task_by_id(task_id, current_user.id)  # type: ignore


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


@assistant_router.get(
    "/assistants/task/{task_id}/download",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
)
async def get_download_link_task(
    request: Request,
    task_id: int,
    current_user: UserIdentityDep,
    tasks_service: TasksServiceDep,
):
    return await tasks_service.get_download_link_task(task_id, current_user.id)
