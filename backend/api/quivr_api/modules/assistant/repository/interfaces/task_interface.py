from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from quivr_api.modules.assistant.dto.inputs import CreateTask
from quivr_api.modules.assistant.entity.task_entity import Task


class TasksInterface(ABC):
    @abstractmethod
    def create_task(self, task: CreateTask) -> Task:
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: UUID, user_id: UUID) -> Task:
        pass

    @abstractmethod
    def delete_task(self, task_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    def get_tasks_by_user_id(self, user_id: UUID) -> List[Task]:
        pass

    @abstractmethod
    def update_task(self, task_id: int, task: dict) -> None:
        pass

    @abstractmethod
    def get_download_link_task(self, task_id: int, user_id: UUID) -> str:
        pass
