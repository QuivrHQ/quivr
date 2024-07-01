from uuid import UUID

from fastapi import HTTPException
from quivr_core.api.models.settings import get_supabase_client
from quivr_core.api.modules.dependencies import BaseRepository
from quivr_core.api.modules.prompt.entity.prompt import DeletePromptResponse, Prompt


class PromptRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.db = get_supabase_client()

    def create_prompt(self, prompt):
        """
        Create a prompt
        """

        response = (self.db.from_("prompts").insert(prompt.dict()).execute()).data

        return Prompt(**response[0])

    def delete_prompt_by_id(self, prompt_id: UUID):
        """
        Delete a prompt by id
        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
        A dictionary containing the status of the delete and prompt_id of the deleted prompt
        """

        # Update brains where prompt_id is equal to the value to NULL
        self.db.from_("brains").update({"prompt_id": None}).filter(
            "prompt_id", "eq", str(prompt_id)
        ).execute()

        # Update chat_history where prompt_id is equal to the value to NULL
        self.db.from_("chat_history").update({"prompt_id": None}).filter(
            "prompt_id", "eq", str(prompt_id)
        ).execute()

        # Delete the prompt
        response = (
            self.db.from_("prompts")
            .delete()
            .filter("id", "eq", str(prompt_id))
            .execute()
            .data
        )

        if response == []:
            raise HTTPException(404, "Prompt not found")

        return DeletePromptResponse(status="deleted", prompt_id=prompt_id)

    def get_prompt_by_id(self, prompt_id: UUID):
        """
        Get a prompt by its id

        Args:
            prompt_id (UUID): The id of the prompt

        Returns:
            Prompt: The prompt
        """

        response = (
            self.db.from_("prompts")
            .select("*")
            .filter("id", "eq", str(prompt_id))
            .execute()
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

    def update_prompt_by_id(self, prompt_id: UUID, prompt):
        """Update a prompt by id"""

        response = (
            self.db.from_("prompts")
            .update(prompt.dict(exclude_unset=True))
            .filter("id", "eq", str(prompt_id))
            .execute()
        ).data

        if response == []:
            raise HTTPException(404, "Prompt not found")

        return Prompt(**response[0])
