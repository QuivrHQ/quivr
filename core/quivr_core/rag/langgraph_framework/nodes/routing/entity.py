from pydantic import BaseModel, Field
from typing import Optional, List


class SplittedInput(BaseModel):
    instructions_reasoning: Optional[str] = Field(
        default=None,
        description="The reasoning that leads to identifying the user instructions to the system",
    )
    instructions: Optional[str] = Field(
        default=None, description="The instructions to the system"
    )

    tasks_reasoning: Optional[str] = Field(
        default=None,
        description="The reasoning that leads to identifying the explicit or implicit user tasks and questions",
    )
    task_list: Optional[List[str]] = Field(
        default_factory=lambda: ["No explicit or implicit tasks found"],
        description="The list of standalone, self-contained tasks or questions.",
    )
