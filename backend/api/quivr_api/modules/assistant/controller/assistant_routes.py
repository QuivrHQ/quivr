import io
from typing import Annotated, List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth.auth_bearer import AuthBearer, get_current_user
from quivr_api.modules.assistant.controller.assistants_definition import (
    assistants,
    validate_assistant_input,
)
from quivr_api.modules.assistant.dto.inputs import CreateTask, InputAssistant
from quivr_api.modules.assistant.dto.outputs import AssistantOutput
from quivr_api.modules.assistant.entity.assistant_entity import (
    AssistantSettings,
)
from quivr_api.modules.assistant.services.tasks_service import TasksService
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.upload.service.upload_file import (
    upload_file_storage,
)
from quivr_api.modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)


assistant_router = APIRouter()


TasksServiceDep = Annotated[TasksService, Depends(get_service(TasksService))]
UserIdentityDep = Annotated[UserIdentity, Depends(get_current_user)]


@assistant_router.get(
    "/assistants", dependencies=[Depends(AuthBearer())], tags=["Assistant"]
)
async def get_assistants(
    request: Request,
    current_user: UserIdentity = Depends(get_current_user),
) -> List[AssistantOutput]:
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
    current_user: UserIdentityDep,
    tasks_service: TasksServiceDep,
    request: Request,
    input: InputAssistant,
    files: List[UploadFile] = None,
):
    assistant = next(
        (assistant for assistant in assistants if assistant.id == input.id), None
    )
    if assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")

    is_valid, validation_errors = validate_assistant_input(input, assistant)
    if not is_valid:
        for error in validation_errors:
            print(error)
            raise HTTPException(status_code=400, detail=error)
    else:
        print("Assistant input is valid.")
    notification_uuid = uuid4()

    # Process files dynamically
    for upload_file in files:
        file_name_path = f"{input.id}/{notification_uuid}/{upload_file.filename}"
        buff_reader = io.BufferedReader(upload_file.file)  # type: ignore
        try:
            await upload_file_storage(buff_reader, file_name_path)
        except Exception as e:
            logger.exception(f"Exception in upload_route {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to upload file to storage. {e}"
            )

    task = CreateTask(
        assistant_id=input.id,
        pretty_id=str(notification_uuid),
        settings=input.model_dump(mode="json"),
    )

    task_created = await tasks_service.create_task(task, current_user.id)

    celery.send_task(
        "process_assistant_task",
        kwargs={
            "assistant_id": input.id,
            "notification_uuid": notification_uuid,
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


@assistant_router.get(
    "/assistants/{assistant_id}/config",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
    response_model=AssistantSettings,
    summary="Retrieve assistant configuration",
    description="Get the settings and file requirements for the specified assistant.",
)
async def get_assistant_config(
    assistant_id: int,
    current_user: UserIdentityDep,
):
    assistant = next(
        (assistant for assistant in assistants if assistant.id == assistant_id), None
    )
    if assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant.settings
