from typing import Sequence
from uuid import UUID

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from quivr_api.modules.assistant.dto.inputs import CreateTask
from quivr_api.modules.assistant.entity.task_entity import Task
from quivr_api.modules.dependencies import BaseRepository


class TasksRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_task(self, task: CreateTask, user_id: UUID) -> Task:
        try:
            task_to_create = Task(pretty_id=task.pretty_id, user_id=user_id)
            self.session.add(task_to_create)
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise Exception()

        await self.session.refresh(task_to_create)
        return task_to_create

    async def get_task_by_id(self, task_id: UUID) -> Task:
        query = select(Task).where(Task.id == task_id)
        response = await self.session.exec(query)
        return response.one()

    async def get_tasks_by_user_id(self, user_id: UUID) -> Sequence[Task]:
        query = select(Task).where(Task.user_id == user_id)
        response = await self.session.exec(query)
        return response.all()

    async def delete_task(self, task_id: int, user_id: UUID) -> None:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        response = await self.session.exec(query)
        task = response.one()
        if task:
            await self.session.delete(task)
            await self.session.commit()
        else:
            raise Exception()
