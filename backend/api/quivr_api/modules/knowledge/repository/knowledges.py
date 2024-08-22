from typing import Sequence
from uuid import UUID

from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException
from quivr_core.models import KnowledgeStatus
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseRepository, get_supabase_client
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
        query = select(KnowledgeDB).where(
            KnowledgeDB.brain_id == knowledge.brain_id,
            KnowledgeDB.file_name == knowledge.file_name,
        )
        result = await self.session.exec(query)
        existing_knowledge = result.first()

        try:
            if existing_knowledge:
                existing_knowledge.source_link = knowledge.source_link
                self.session.add(existing_knowledge)
                # create link
                assert existing_knowledge.id, "Knowledge ID not generated"
                knowledge_brain = KnowledgeBrain(
                    brain_id=existing_knowledge.brain_id,
                    knowledge_id=existing_knowledge.id,
                )
                self.session.add(knowledge_brain)
            else:
                self.session.add(knowledge)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise Exception("Integrity error while creating notion files.")
        except Exception as e:
            await self.session.rollback()
            raise e
        return knowledge

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
        assert isinstance(knowledge.file_name, str), "file_name should be a string"
        return DeleteKnowledgeResponse(
            file_name=knowledge.file_name,
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

    async def remove_brain_all_knowledge(self, brain_id) -> int:
        """
        Remove all knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        all_knowledge = await self.get_all_knowledge_in_brain(brain_id)
        knowledge_to_delete_list = [
            knowledge.source_link
            for knowledge in all_knowledge
            if knowledge.source == "local"
        ]

        if knowledge_to_delete_list:
            # FIXME: Can we bypass db ? @Amine
            self.db.storage.from_("quivr").remove(knowledge_to_delete_list)

        select_query = select(KnowledgeDB).where(KnowledgeDB.brain_id == brain_id)
        items_to_delete = await self.session.exec(select_query)
        for item in items_to_delete:
            await self.session.delete(item)
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

    async def update_file_sha1_knowledge(
        self, knowledge_id: UUID, file_sha1: str
    ) -> KnowledgeDB | None:
        query = select(KnowledgeDB).where(KnowledgeDB.id == knowledge_id)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            return None

        try:
            knowledge.file_sha1 = file_sha1
            self.session.add(knowledge)
            await self.session.commit()
            await self.session.refresh(knowledge)
            return knowledge
        except (UniqueViolationError, IntegrityError, Exception):
            await self.session.rollback()
            raise FileExistsError(
                f"File {knowledge_id} already exists maybe under another file_name"
            )

    async def get_all_knowledge(self) -> Sequence[KnowledgeDB]:
        query = select(KnowledgeDB)
        result = await self.session.exec(query)
        return result.all()
