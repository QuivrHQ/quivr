from uuid import UUID

from fastapi import HTTPException
from quivr_api.models.settings import get_supabase_client
from quivr_api.modules.knowledge.dto.inputs import KnowledgeStatus
from quivr_api.modules.knowledge.dto.outputs import DeleteKnowledgeResponse
from quivr_api.modules.knowledge.repository.knowledge_interface import (
    KnowledgeInterface,
)
from quivr_core.models import QuivrKnowledge as Knowledge


class KnowledgeRepository(KnowledgeInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def insert_knowledge(self, knowledge):
        """
        Add a knowledge
        """
        # Check if the knowledge already exists
        knowledge_exists = (
            self.db.from_("knowledge")
            .select("*")
            .filter("brain_id", "eq", str(knowledge.brain_id))
            .filter("file_name", "eq", str(knowledge.file_name))
            .execute()
        ).data

        if knowledge_exists:
            return Knowledge(**knowledge_exists[0])  # TODO fix this

        response = (self.db.from_("knowledge").insert(knowledge.dict()).execute()).data
        return Knowledge(**response[0])

    def remove_knowledge_by_id(
        # todo: update remove brain endpoints to first delete the knowledge
        self,
        knowledge_id,
    ):
        """
        Args:
            knowledge_id (UUID): The id of the knowledge

        Returns:
            str: Status message
        """
        response = (
            self.db.from_("knowledge")
            .delete()
            .filter("id", "eq", str(knowledge_id))
            .execute()
            .data
        )

        if response == []:
            raise HTTPException(404, "Knowledge not found")

        return DeleteKnowledgeResponse(
            # change to response[0].brain_id and knowledge_id[0].brain_id
            status="deleted",
            knowledge_id=knowledge_id,
        )

    def get_knowledge_by_id(self, knowledge_id):
        """
        Get a knowledge by its id
        Args:
            brain_id (UUID): The id of the brain
        """
        knowledge = (
            self.db.from_("knowledge")
            .select("*")
            .filter("id", "eq", str(knowledge_id))
            .execute()
        ).data

        return Knowledge(**knowledge[0])

    def get_all_knowledge_in_brain(self, brain_id: UUID) -> list[Knowledge]:
        """
        Get all the knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        all_knowledge = (
            self.db.from_("knowledge")
            .select("*")
            .filter("brain_id", "eq", str(brain_id))
            .execute()
        ).data

        return [Knowledge(**knowledge) for knowledge in all_knowledge]

    def remove_brain_all_knowledge(self, brain_id):
        """
        Remove all knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        all_knowledge = self.get_all_knowledge_in_brain(brain_id)
        knowledge_to_delete_list = []

        for knowledge in all_knowledge:
            if knowledge.file_name:
                knowledge_to_delete_list.append(f"{brain_id}/{knowledge.file_name}")

        if knowledge_to_delete_list:
            self.db.storage.from_("quivr").remove(knowledge_to_delete_list)

        self.db.from_("knowledge").delete().filter(
            "brain_id", "eq", str(brain_id)
        ).execute()

    def update_status_knowledge(self, knowledge_id: UUID, status: KnowledgeStatus):
        """
        Update the status of a knowledge
        """
        updated_knowledge = (
            self.db.from_("knowledge")
            .update({"status": status})
            .filter("id", "eq", str(knowledge_id))
            .execute()
        ).data

        return True
