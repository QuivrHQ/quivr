from typing import List
from uuid import UUID

from quivr_core.api.modules.brain.service.utils.get_prompt_to_use_id import (
    get_prompt_to_use_id,
)
from quivr_core.api.modules.dependencies import BaseService
from quivr_core.api.modules.prompt.entity.prompt import (
    CreatePromptProperties,
    DeletePromptResponse,
    Prompt,
    PromptUpdatableProperties,
)
from quivr_core.api.modules.prompt.repository.prompts import PromptRepository


class PromptService(BaseService[PromptRepository]):
    repository: PromptRepository

    def __init__(self, repository: PromptRepository):
        self.repository = repository

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

    def get_prompt_to_use(
        self, brain_id: UUID | None, prompt_id: UUID | None
    ) -> Prompt | None:
        prompt_to_use_id = get_prompt_to_use_id(brain_id, prompt_id)

        if prompt_to_use_id is None:
            return None

        return self.get_prompt_by_id(prompt_to_use_id)
