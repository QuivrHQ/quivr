from typing import List
from uuid import UUID

from models.settings import get_supabase_client
from modules.prompt.entity.prompt import (
    CreatePromptProperties,
    DeletePromptResponse,
    Prompt,
    PromptUpdatableProperties,
)
from modules.prompt.repository.prompts import Prompts


class PromptService:
    repository: Prompts

    def __init__(self):
        supabase_client = get_supabase_client()
        self.repository = Prompts()

    def create_prompt(self, prompt: CreatePromptProperties) -> Prompt:
        return self.repository.create_prompt(prompt)

    def delete_prompt_by_id(self, prompt_id: UUID) -> DeletePromptResponse:
        """
        Delete a prompt by id
        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
            Prompt: The prompt
        """
        return self.repository.delete_prompt_by_id(prompt_id)

    def get_prompt_by_id(self, prompt_id: UUID) -> Prompt | None:
        """
        Get a prompt by its id

        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
            Prompt: The prompt
        """
        return self.repository.get_prompt_by_id(prompt_id)

    def get_public_prompts(self) -> List[Prompt]:
        """
        List all public prompts
        """

        return self.repository.get_public_prompts()

    def update_prompt_by_id(
        self, prompt_id: UUID, prompt: PromptUpdatableProperties
    ) -> Prompt:
        """Update a prompt by id"""

        return self.repository.update_prompt_by_id(prompt_id, prompt)
