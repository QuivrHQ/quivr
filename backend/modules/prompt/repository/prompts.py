from fastapi import HTTPException
from modules.prompt.entity.prompt import Prompt
from modules.prompt.repository.prompts_interface import (
    DeletePromptResponse,
    PromptsInterface,
)
from models.settings import get_supabase_client


class Prompts(PromptsInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def create_prompt(self, prompt):
        """
        Create a prompt
        """

        response = (self.db.from_("prompts").insert(prompt.dict()).execute()).data

        return Prompt(**response[0])

    def delete_prompt_by_id(self, prompt_id):
        """
        Delete a prompt by id
        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
        A dictionary containing the status of the delete and prompt_id of the deleted prompt
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

        return DeletePromptResponse(status="deleted", prompt_id=prompt_id)

    def get_prompt_by_id(self, prompt_id):
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

    def get_public_prompts(self):
        """
        List all public prompts
        """

        return (
            self.db.from_("prompts")
            .select("*")
            .filter("status", "eq", "public")
            .execute()
        ).data

    def update_prompt_by_id(self, prompt_id, prompt):
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
