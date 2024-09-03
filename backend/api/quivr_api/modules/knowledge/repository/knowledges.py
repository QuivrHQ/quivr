from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from quivr_core.models import KnowledgeStatus
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select, text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import Brain
from quivr_api.modules.dependencies import BaseRepository, get_supabase_client
from quivr_api.modules.knowledge.dto.outputs import DeleteKnowledgeResponse
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB

logger = get_logger(__name__)


class KnowledgeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        supabase_client = get_supabase_client()
        self.db = supabase_client

    async def insert_knowledge(
        self, knowledge: KnowledgeDB, brain_id: UUID
    ) -> KnowledgeDB:
        logger.debug(f"Inserting knowledge {knowledge}")
        query = select(Brain).where(Brain.brain_id == brain_id)
        result = await self.session.exec(query)
        brain = result.first()
        logger.debug(f"Found associated brain: {brain}")
        if not brain:
            raise HTTPException(404, "Brain not found")
        try:
            knowledge.brains.append(brain)
            self.session.add(knowledge)
            await self.session.commit()
            await self.session.refresh(knowledge)
        except IntegrityError:
            await self.session.rollback()
            raise
        except Exception:
            await self.session.rollback()
            raise
        return knowledge

    async def link_to_brain(
        self, knowledge: KnowledgeDB, brain_id: UUID
    ) -> KnowledgeDB:
        logger.debug(f"Linking knowledge {knowledge.id} to {brain_id}")
        brain = await self.get_brain_by_id(brain_id)
        knowledge.brains.append(brain)
        self.session.add(knowledge)
        await self.session.commit()
        await self.session.refresh(knowledge)
        return knowledge

    async def remove_knowledge_from_brain(
        self, knowledge_id: UUID, brain_id: UUID
    ) -> KnowledgeDB:
        knowledge = await self.get_knowledge_by_id(knowledge_id)
        brain = await self.get_brain_by_id(brain_id)
        existing_brains = await knowledge.awaitable_attrs.brains
        existing_brains.remove(brain)
        knowledge.brains = existing_brains
        self.session.add(knowledge)
        await self.session.commit()
        await self.session.refresh(knowledge)
        return knowledge

    async def remove_knowledge_by_id(
        self, knowledge_id: UUID
    ) -> DeleteKnowledgeResponse:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise NoResultFound("Knowledge not found")

        await self.session.delete(knowledge)
        await self.session.commit()
        assert isinstance(knowledge.file_name, str), "file_name should be a string"
        return DeleteKnowledgeResponse(
            file_name=knowledge.file_name,
            status="deleted",
            knowledge_id=knowledge_id,
        )

    async def get_knowledge_by_sync_id(self, sync_id: int) -> KnowledgeDB:
        query = select(KnowledgeDB).where(
            text(f"metadata->>'sync_file_id' =  '{str(sync_id)}'")
        )
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise HTTPException(404, "Knowledge not found")

        return knowledge

    async def get_knowledge_by_sha1(self, sha1: str) -> KnowledgeDB:
        query = select(KnowledgeDB).where(KnowledgeDB.file_sha1 == sha1)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise NoResultFound("Knowledge not found")

        return knowledge

    async def get_knowledge_by_id(self, knowledge_id: UUID) -> KnowledgeDB:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise NoResultFound("Knowledge not found")

        return knowledge

    async def get_brain_by_id(self, brain_id: UUID) -> Brain:
        query = select(Brain).where(Brain.brain_id == brain_id)
        result = await self.session.exec(query)
        brain = result.first()
        if not brain:
            raise NoResultFound("Brain not found")
        return brain

    async def remove_all_knowledges_from_brain(self, brain_id) -> int:
        """
        Remove all knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        brain = await self.get_brain_by_id(brain_id)
        all_knowledge = await brain.awaitable_attrs.knowledges
        knowledge_to_delete_list = [
            knowledge.knowledge.source_link
            for knowledge in all_knowledge
            if knowledge.source == "local"
        ]

        if knowledge_to_delete_list:
            # FIXME: Can we bypass db ? @Amine
            self.db.storage.from_("quivr").remove(knowledge_to_delete_list)

        for item in all_knowledge:
            await self.session.delete(item)
        await self.session.commit()
        await self.session.refresh(brain)
        return len(knowledge_to_delete_list)

    async def update_status_knowledge(
        self, knowledge_id: UUID, status: KnowledgeStatus
    ) -> KnowledgeDB | None:
        try:
            query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
            result = await self.session.exec(query)
            knowledge = result.first()
            if not knowledge:
                raise NoResultFound("Knowledge not found")

            knowledge.status = status
            self.session.add(knowledge)
            await self.session.commit()
            await self.session.refresh(knowledge)
            return knowledge
        except Exception:
            await self.session.rollback()
            raise NoResultFound("Knowledge not found")

    async def update_source_link_knowledge(
        self, knowledge_id: UUID, source_link: str
    ) -> KnowledgeDB:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise NoResultFound("Knowledge not found")

        knowledge.source_link = source_link
        self.session.add(knowledge)
        await self.session.commit()
        await self.session.refresh(knowledge)

        return knowledge

    async def update_file_sha1_knowledge(
        self, knowledge_id: UUID, file_sha1: str
    ) -> KnowledgeDB | None:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise ValueError("Knowledge not found")

        try:
            knowledge.file_sha1 = file_sha1
            self.session.add(knowledge)
            await self.session.commit()
            await self.session.refresh(knowledge)
            return knowledge
        except IntegrityError:
            await self.session.rollback()
            raise FileExistsError(
                f"File {knowledge_id} already exists maybe under another file_name"
            )

    async def get_all_knowledge(self) -> Sequence[KnowledgeDB]:
        query = select(KnowledgeDB)
        result = await self.session.exec(query)
        return result.all()
