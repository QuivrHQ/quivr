from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from quivr_api.models.settings import get_supabase_client
from quivr_api.modules.dependencies import BaseRepository
from quivr_api.modules.knowledge.dto.inputs import KnowledgeStatus
from quivr_api.modules.knowledge.dto.outputs import DeleteKnowledgeResponse
#from quivr_core.models import QuivrKnowledge as Knowledge
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class KnowledgeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        supabase_client = get_supabase_client()
        self.db = supabase_client

    async def insert_knowledge(self, knowledge: KnowledgeDB) -> KnowledgeDB:
        query = select(KnowledgeDB).where(
            KnowledgeDB.brain_id == knowledge.brain_id,
            KnowledgeDB.file_name == knowledge.file_name
        )
        result = await self.session.exec(query)
        existing_knowledge = result.first()

        if existing_knowledge:
            return existing_knowledge

        self.session.add(knowledge)
        await self.session.commit()
        await self.session.refresh(knowledge)
        return knowledge

    async def remove_knowledge_by_id(self, knowledge_id: UUID) -> DeleteKnowledgeResponse:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise HTTPException(404, "Knowledge not found")

        await self.session.delete(knowledge)
        await self.session.commit()

        return DeleteKnowledgeResponse(
            status="deleted",
            knowledge_id=knowledge_id,
        )

    async def get_knowledge_by_id(self, knowledge_id: UUID) -> KnowledgeDB:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise HTTPException(404, "Knowledge not found")

        return knowledge

    async def get_all_knowledge_in_brain(self, brain_id: UUID) -> Sequence[KnowledgeDB]:
        query = select(KnowledgeDB).where(KnowledgeDB.brain_id == brain_id)
        result = await self.session.exec(query)
        return result.all()

    async def remove_brain_all_knowledge(self, brain_id):
        """
        Remove all knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        all_knowledge = await self.get_all_knowledge_in_brain(brain_id)
        knowledge_to_delete_list = []

        for knowledge in all_knowledge:
            if knowledge.file_name:
                knowledge_to_delete_list.append(f"{brain_id}/{knowledge.file_name}")

        if knowledge_to_delete_list:
            #FIXME: Can we bypass db ? @Amine
            self.db.storage.from_("quivr").remove(knowledge_to_delete_list)

        select_query = select(KnowledgeDB).where(KnowledgeDB.brain_id == brain_id)
        items_to_delete = await self.session.exec(select_query)
        for item in items_to_delete:
            await self.session.delete(item)
        await self.session.commit()

    async def update_status_knowledge(self, knowledge_id: UUID, status: KnowledgeStatus) -> bool:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            return False

        knowledge.status = status
        self.session.add(knowledge)
        await self.session.commit()
        await self.session.refresh(knowledge)

        return True

    async def get_all_knowledge(self) -> Sequence[KnowledgeDB]:
        query = select(KnowledgeDB)
        result = await self.session.exec(query)
        return result.all()
