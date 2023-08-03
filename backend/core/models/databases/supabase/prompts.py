from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from models.databases.repository import Repository
from models.prompt import Prompt
from pydantic import BaseModel


class CreatePromptProperties(BaseModel):
    """Properties that can be received on prompt creation"""

    title: str
    content: str
    status: str = "private"


class PromptUpdatableProperties(BaseModel):
    """Properties that can be received on prompt update"""

    title: Optional[str]
    content: Optional[str]
    status: Optional[str]


class Prompts(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def create_prompt(self, prompt: CreatePromptProperties) -> Prompt:
        """Create a prompt by id"""

        response = (self.db.from_("prompts").insert(prompt.dict()).execute()).data

        return Prompt(**response[0])

    def delete_prompt_by_id(self, prompt_id: UUID) -> Prompt | None:
        """
        Delete a prompt by id
        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
            Prompt: The prompt
        """
        response = (
            self.db.from_("prompts")
            .delete()
            .filter("id", "eq", prompt_id)
            .execute()
            .data
        )
        if response == []:
            raise HTTPException(404, "Prompt not found")
        return Prompt(**response[0])

    def get_prompt_by_id(self, prompt_id: UUID) -> Prompt | None:
        """
        Get a prompt by its id

        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
            Prompt: The prompt
        """

        response = (
            self.db.from_("prompts").select("*").filter("id", "eq", prompt_id).execute()
        ).data

        if response == []:
            return None
        return Prompt(**response[0])

    def get_public_prompts(self) -> list[Prompt]:
        """
        List all public prompts
        """

        return (
            self.db.from_("prompts")
            .select("*")
            .filter("status", "eq", "public")
            .execute()
        ).data

    def update_prompt_by_id(
        self, prompt_id: UUID, prompt: PromptUpdatableProperties
    ) -> Prompt:
        """Update a prompt by id"""

        response = (
            self.db.from_("prompts")
            .update(prompt.dict(exclude_unset=True))
            .filter("id", "eq", prompt_id)
            .execute()
        ).data

        if response == []:
            raise HTTPException(404, "Prompt not found")

        return Prompt(**response[0])
