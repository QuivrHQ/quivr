from typing import Annotated, List
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
    task = CreateTask(
        pretty_id="hello mama"
    )
    
    if assistant_id not in [assistant.id for assistant in assistants]:
        raise HTTPException(status_code=404, detail="Assistant not found")
    
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
