from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4, UUID
from langchain_core.documents import Document


class UserTaskEntity(BaseModel):
    id: UUID
    definition: str
    docs: List[Document] = Field(default_factory=list)
    completable: bool = Field(
        default=False, description="Whether the task has been completed or not"
    )
    tool: Optional[str] = Field(
        default=None, description="The tool that shall be used to complete the task"
    )

    def has_tool(self) -> bool:
        return bool(self.tool)

    def is_completable(self) -> bool:
        return self.completable


class UserTasks:
    def __init__(self, task_definitions: List[str] | None = None):
        self.user_tasks = {}
        if task_definitions:
            for definition in task_definitions:
                id = uuid4()
                self.user_tasks[id] = UserTaskEntity(
                    id=id, definition=definition, docs=[]
                )

    def __iter__(self):
        return iter(self.user_tasks.values())

    def set_docs(self, id: UUID, docs: List[Document]):
        if self.user_tasks:
            if id in self.user_tasks:
                self.user_tasks[id].docs = docs
            else:
                raise ValueError(f"Task with id {id} not found")

    def set_definition(self, id: UUID, definition: str):
        if self.user_tasks:
            if id in self.user_tasks:
                self.user_tasks[id].definition = definition
            else:
                raise ValueError(f"Task with id {id} not found")

    def set_completion(self, id: UUID, completable: bool):
        if self.user_tasks:
            if id in self.user_tasks:
                self.user_tasks[id].completable = completable
            else:
                raise ValueError(f"Task with id {id} not found")

    def set_tool(self, id: UUID, tool: str):
        if self.user_tasks:
            if id in self.user_tasks:
                self.user_tasks[id].tool = tool
            else:
                raise ValueError(f"Task with id {id} not found")

    def __call__(self, id: UUID) -> UserTaskEntity:
        return self.user_tasks[id]

    def has_tasks(self) -> bool:
        return bool(self.user_tasks)

    def has_non_completable_tasks(self) -> bool:
        return bool(self.non_completable_tasks)

    @property
    def non_completable_tasks(self) -> List[UserTaskEntity]:
        return [task for task in self.user_tasks.values() if not task.is_completable()]

    @property
    def completable_tasks(self) -> List[UserTaskEntity]:
        return [task for task in self.user_tasks.values() if task.is_completable()]

    @property
    def ids(self) -> List[UUID]:
        return list(self.user_tasks.keys())

    @property
    def definitions(self) -> List[str]:
        return [task.definition for task in self.user_tasks.values()]

    @property
    def docs(self) -> List[Document]:
        # Return the concatenation of all docs
        return [doc for task in self.user_tasks.values() for doc in task.docs]
