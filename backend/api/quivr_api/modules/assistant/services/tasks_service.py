from typing import Sequence
from uuid import UUID

from quivr_api.modules.assistant.dto.inputs import CreateTask
from quivr_api.modules.assistant.entity.task_entity import Task
from quivr_api.modules.assistant.repository.tasks import TasksRepository
from quivr_api.modules.dependencies import BaseService


class TasksService(BaseService[TasksRepository]):
    repository_cls = TasksRepository

    def __init__(self, repository: TasksRepository):
        self.repository = repository

    async def create_task(self, task: CreateTask, user_id: UUID) -> Task:
        return await self.repository.create_task(task, user_id)

    async def get_task_by_id(self, task_id: UUID, user_id: UUID) -> Task:
        return await self.repository.get_task_by_id(task_id, user_id)

    async def get_tasks_by_user_id(self, user_id: UUID) -> Sequence[Task]:
        return await self.repository.get_tasks_by_user_id(user_id)

    async def delete_task(self, task_id: int, user_id: UUID) -> None:
        return await self.repository.delete_task(task_id, user_id)

    async def update_task(self, task_id: int, task: dict) -> None:
        return await self.repository.update_task(task_id, task)

    async def get_download_link_task(self, task_id: int, user_id: UUID) -> str:
        return await self.repository.get_download_link_task(task_id, user_id)
