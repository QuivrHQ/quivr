from abc import ABC, abstractmethod
from uuid import UUID

from modules.prompt.entity import (
    CreatePromptProperties,
    DeletePromptResponse,
    Prompt,
    PromptUpdatableProperties,
)


class PromptsInterface(ABC):
    @abstractmethod
    def create_prompt(self, prompt: CreatePromptProperties) -> Prompt:
        """
        Create a prompt
        """
        pass

    @abstractmethod
    def delete_prompt_by_id(self, prompt_id: UUID) -> DeletePromptResponse:
        """
        Delete a prompt by id
        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
        A dictionary containing the status of the delete and prompt_id of the deleted prompt
        """
        pass

    @abstractmethod
    def get_prompt_by_id(self, prompt_id: UUID) -> Prompt | None:
        """
        Get a prompt by its id

        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
            Prompt: The prompt
        """
        pass

    @abstractmethod
    def get_public_prompts(self) -> list[Prompt]:
        """
        List all public prompts
        """
        pass

    @abstractmethod
    def update_prompt_by_id(
        self, prompt_id: UUID, prompt: PromptUpdatableProperties
    ) -> Prompt:
        """Update a prompt by id"""
        pass
