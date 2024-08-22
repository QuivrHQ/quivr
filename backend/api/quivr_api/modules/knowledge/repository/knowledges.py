from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseRepository, get_supabase_client
from quivr_api.modules.knowledge.dto.inputs import KnowledgeStatus
from quivr_api.modules.knowledge.dto.outputs import DeleteKnowledgeResponse
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.knowledge.entity.knowledge_brain import KnowledgeBrain

logger = get_logger(__name__)


class KnowledgeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        supabase_client = get_supabase_client()
        self.db = supabase_client

    async def insert_knowledge(self, knowledge: KnowledgeDB) -> KnowledgeDB:
        logger.debug(f"Inserting knowledge {knowledge}")
        try:
            self.session.add(knowledge)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise Exception("Integrity error while creating knowledge.")
        except Exception as e:
            await self.session.rollback()
            raise e
        return knowledge

    async def insert_knowledge_brain(
        self, knowledge_brain: KnowledgeBrain
    ) -> KnowledgeBrain:
        logger.debug(f"Inserting knowledge brain {knowledge_brain}")
        try:
            self.session.add(knowledge_brain)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise Exception("Integrity error while creating knowledge brain.")
        except Exception as e:
            await self.session.rollback()
            raise e
        return knowledge_brain

    async def remove_knowledge_by_id(
        self, knowledge_id: UUID
    ) -> DeleteKnowledgeResponse:
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

    async def get_all_knowledge_in_brain(
        self, brain_id: UUID
    ) -> Sequence[KnowledgeBrain]:
        # Get all knowledge_id in a brain
        query = (
            select(KnowledgeBrain)
            .options(joinedload(KnowledgeBrain.knowledge))
            .where(KnowledgeBrain.brain_id == brain_id)
        )
        result = await self.session.exec(query)
        return result.all()

    async def remove_brain_all_knowledge(self, brain_id) -> int:
        """
        Remove all knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        all_knowledge_brain = await self.get_all_knowledge_in_brain(brain_id)
        knowledge_to_delete_list = [
            knowledge_brain.knowledge.source_link
            for knowledge_brain in all_knowledge_brain
            if knowledge_brain.knowledge.source == "local"
        ]

        if knowledge_to_delete_list:
            # FIXME: Can we bypass db ? @Amine
            self.db.storage.from_("quivr").remove(knowledge_to_delete_list)

        for item in all_knowledge_brain:
            await self.session.delete(item.knowledge)
        await self.session.commit()
        return len(knowledge_to_delete_list)

    async def update_status_knowledge(
        self, knowledge_id: UUID, status: KnowledgeStatus
    ) -> KnowledgeDB | None:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            return None

        knowledge.status = status
        self.session.add(knowledge)
        await self.session.commit()
        await self.session.refresh(knowledge)

        return knowledge

    async def update_source_link_knowledge(
        self, knowledge_id: UUID, source_link: str
    ) -> KnowledgeDB:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise HTTPException(404, "Knowledge not found")

        knowledge.source_link = source_link
        self.session.add(knowledge)
        await self.session.commit()
        await self.session.refresh(knowledge)

        return knowledge

    async def get_all_knowledge(self) -> Sequence[KnowledgeDB]:
        query = select(KnowledgeDB)
        result = await self.session.exec(query)
        return result.all()
