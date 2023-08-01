from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from models.prompt import Prompt
from models.settings import common_dependencies
from pydantic import BaseModel


class PromptUpdatableProperties(BaseModel):
    """Properties that can be received on prompt update"""

    title: Optional[str]
    content: Optional[str]
    status: Optional[str]


def update_prompt_by_id(prompt_id: UUID, prompt: PromptUpdatableProperties) -> Prompt:
    """Update a prompt by id"""
    commons = common_dependencies()

    response = (
        commons["supabase"]
        .from_("prompts")
        .update(prompt.dict(exclude_unset=True))
        .filter("id", "eq", prompt_id)
        .execute()
    ).data

    if response == []:
        raise HTTPException(404, "Prompt not found")

    return Prompt(**response[0])
