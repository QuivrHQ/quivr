from typing import List
from uuid import UUID

from fastapi import HTTPException
from models.databases.repository import Repository
from models.knowledge import BrainKnowledge
from pydantic import BaseModel


class CreateBrainKnowledgeProperties(BaseModel):
    """Properties that can be received on brain knowledge creation"""

    brain_id: UUID
    knowledge_id: UUID

    def dict(self, *args, **kwargs):
        brain_knowledge_dict = super().dict(*args, **kwargs)
        brain_knowledge_dict["brain_id"] = str(brain_knowledge_dict.get("brain_id"))
        brain_knowledge_dict["knowledge_id"] = str(
            brain_knowledge_dict.get("knowledge_id")
        )
        return brain_knowledge_dict


class DeleteKnowledgeRelatedToBrainResponse(BaseModel):
    """Response when deleting all the knowledge related to a brain"""

    status: str = "delete"
    brain_id: UUID
    knowledge_ids: List[UUID]


class DeleteBrainKnowledgeResponse(BaseModel):
    """Response when deleting a brain knowledge"""

    status: str = "delete"
    brain_id: UUID
    knowledge_id: UUID


class BrainKnowledges(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def insert_brain_knowledge(
        self, brain_knowledge: CreateBrainKnowledgeProperties
    ) -> BrainKnowledge:
        """
        Add a brain knowledge
        """
        response = (
            self.db.from_("brain_knowledge").insert(brain_knowledge.dict()).execute()
        ).data
        return BrainKnowledge(**response[0])

    def remove_brain_knowledge_by_brain_id(
        self, brain_id: UUID
    ) -> DeleteKnowledgeRelatedToBrainResponse:
        """
        Remove a brain by id
        Args:
            brain_id (UUID): The id of the brain

        Returns:
            str: Status message
        """
        response = (
            self.db.from_("brain_knowledge")
            .delete()
            .filter("brain_id", "eq", brain_id)
            .execute()
            .data
        )

        if response == []:
            raise HTTPException(404, "BrainKnowledge not found")

        return DeleteKnowledgeRelatedToBrainResponse(
            status="deleted", brain_id=brain_id, knowledge_ids=[]
        )

    def remove_brain_knowledge_by_knowledge_id(
        # todo: remove brain
        self,
        brain_id: UUID,
        knowledge_id: UUID,
    ) -> DeleteBrainKnowledgeResponse:
        """
        Remove a brain by id
        Args:
            brain_id (UUID): The id of the brain

        Returns:
            str: Status message
        """
        response = (
            self.db.from_("brain_knowledge")
            .delete()
            .filter("knowledge_id", "eq", knowledge_id)
            .execute()
            .data
        )

        if response == []:
            raise HTTPException(404, "BrainKnowledge not found")

        return DeleteBrainKnowledgeResponse(
            # change to response[0].brain_id and knowledge_id[0].brain_id
            status="deleted",
            brain_id=brain_id,
            knowledge_id=knowledge_id,
        )

    def get_brain_knowledge_by_brain_id(self, brain_id: UUID) -> list[BrainKnowledge]:
        """
        Get all the knowledge from a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        knowledge_list = (
            self.db.from_("brain_knowledge")
            .select("*")
            .filter("brain_id", "eq", brain_id)
            .execute()
        ).data

        return [BrainKnowledge(**knowledge) for knowledge in knowledge_list]
