from typing import Any, List, Sequence
from uuid import UUID

from fastapi import HTTPException
from quivr_core.models import KnowledgeStatus
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import joinedload
from sqlmodel import and_, col, select, text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import Brain, BrainUserDB, RoleEnum
from quivr_api.modules.dependencies import BaseRepository, get_supabase_client
from quivr_api.modules.knowledge.dto.inputs import KnowledgeUpdate
from quivr_api.modules.knowledge.dto.outputs import (
    DeleteKnowledgeResponse,
    KnowledgeDTO,
)
from quivr_api.modules.knowledge.entity.knowledge import (
    KnowledgeDB,
)
from quivr_api.modules.knowledge.service.knowledge_exceptions import (
    KnowledgeCreationError,
    KnowledgeNotFoundException,
    KnowledgeUpdateError,
)

logger = get_logger(__name__)


class KnowledgeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        supabase_client = get_supabase_client()
        self.db = supabase_client

    async def create_knowledge(self, knowledge: KnowledgeDB) -> KnowledgeDB:
        try:
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

    async def update_knowledge(
        self,
        knowledge: KnowledgeDB,
        payload: KnowledgeDTO | KnowledgeUpdate | dict[str, Any],
    ) -> KnowledgeDB:
        try:
            logger.debug(f"updating {knowledge.id} with payload {payload}")
            if isinstance(payload, dict):
                update_data = payload
            else:
                update_data = payload.model_dump(exclude_unset=True)
            for field in update_data:
                setattr(knowledge, field, update_data[field])

            self.session.add(knowledge)
            await self.session.commit()
            await self.session.refresh(knowledge)
            return knowledge
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Error updating knowledge {e}")
            raise KnowledgeUpdateError

    async def unlink_knowledge_tree_brains(
        self, knowledge: KnowledgeDB, brains_ids: List[UUID], user_id: UUID
    ) -> list[KnowledgeDB] | None:
        assert knowledge.id, "can't link knowledge not in db"
        try:
            # TODO: Move check somewhere else
            stmt = (
                select(Brain)
                .join(BrainUserDB, col(Brain.brain_id) == col(BrainUserDB.brain_id))
                .where(
                    and_(
                        col(Brain.brain_id).in_(brains_ids),
                        BrainUserDB.user_id == user_id,
                        BrainUserDB.rights == RoleEnum.Owner,
                    )
                )
            )
            unlink_brains = list((await self.session.exec(stmt)).unique().all())
            unlink_brain_ids = {b.brain_id for b in unlink_brains}

            if len(unlink_brains) == 0:
                logger.info(
                    f"No brains for user_id={user_id}, brains_list={brains_ids}"
                )
                return
            children = await self.get_knowledge_tree(knowledge.id)
            all_kms = [knowledge, *children]
            for k in all_kms:
                k.brains = list(
                    filter(lambda b: b.brain_id not in unlink_brain_ids, k.brains)
                )
            [self.session.add(k) for k in all_kms]
            await self.session.commit()
            [await self.session.refresh(k) for k in all_kms]
            return all_kms
        except IntegrityError:
            await self.session.rollback()
            raise
        except Exception:
            await self.session.rollback()
            raise

    async def link_knowledge_tree_brains(
        self, knowledge: KnowledgeDB, brains_ids: List[UUID], user_id: UUID
    ) -> list[KnowledgeDB]:
        assert knowledge.id, "can't link knowledge not in db"
        # TODO(@aminediro @StanGirard): verification should be done elsewhere
        # should rewrite BrainService and Brain Authorization to be as middleware
        try:
            stmt = (
                select(Brain)
                .join(BrainUserDB, col(Brain.brain_id) == col(BrainUserDB.brain_id))
                .where(
                    and_(
                        col(Brain.brain_id).in_(brains_ids),
                        BrainUserDB.user_id == user_id,
                        BrainUserDB.rights == RoleEnum.Owner,
                    )
                )
            )
            brains = list((await self.session.exec(stmt)).unique().all())
            if len(brains) == 0:
                logger.error(
                    f"No brains for user_id={user_id}, brains_list={brains_ids}"
                )
                raise KnowledgeCreationError("can't associate knowledge to brains")
            children = await self.get_knowledge_tree(knowledge.id)
            all_kms = [knowledge, *children]
            for k in all_kms:
                km_brains = {km_brain.brain_id for km_brain in k.brains}
                for b in filter(
                    lambda b: b.brain_id not in km_brains,
                    brains,
                ):
                    k.brains.append(b)
            for k in all_kms:
                await self.session.merge(k)
            await self.session.commit()
            [await self.session.refresh(k) for k in all_kms]
            return all_kms
        except IntegrityError:
            await self.session.rollback()
            raise
        except Exception:
            await self.session.rollback()
            raise

    async def insert_knowledge_brain(
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

    async def remove_knowledge(self, knowledge: KnowledgeDB) -> DeleteKnowledgeResponse:
        assert knowledge.id
        await self.session.delete(knowledge)
        await self.session.commit()
        return DeleteKnowledgeResponse(
            status="deleted", knowledge_id=knowledge.id, file_name=knowledge.file_name
        )

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

    async def get_all_knowledge_sync_user(
        self, sync_id: int, user_id: UUID | None = None
    ) -> List[KnowledgeDB]:
        query = select(KnowledgeDB).where(KnowledgeDB.sync_id == sync_id)
        if user_id:
            query = query.where(KnowledgeDB.user_id == user_id)

        result = await self.session.exec(query)
        return list(result.unique().all())

    async def get_knowledge_by_file_name_brain_id(
        self, file_name: str, brain_id: UUID
    ) -> KnowledgeDB:
        query = (
            select(KnowledgeDB)
            .where(KnowledgeDB.file_name == file_name)
            .where(KnowledgeDB.brains.any(brain_id=brain_id))  # type: ignore
        )

        result = await self.session.exec(query)
        knowledge = result.first()
        if not knowledge:
            raise NoResultFound("Knowledge not found")

        return knowledge

    async def get_knowledge_by_sha1(self, sha1: str) -> KnowledgeDB:
        query = select(KnowledgeDB).where(KnowledgeDB.file_sha1 == sha1)
        result = await self.session.exec(query)
        knowledge = result.first()

        if not knowledge:
            raise NoResultFound("Knowledge not found")

        return knowledge

    async def get_knowledge_tree(self, parent_id: UUID) -> list[KnowledgeDB]:
        from sqlalchemy.orm import aliased

        Knowledge = aliased(KnowledgeDB)
        KnowledgeRecursive = aliased(KnowledgeDB)

        recursive_cte = (
            select(KnowledgeRecursive)
            .where(KnowledgeRecursive.parent_id == parent_id)
            .cte(name="knowledge_tree", recursive=True)
        )

        recursive_cte = recursive_cte.union_all(
            select(Knowledge).join(
                recursive_cte, col(Knowledge.parent_id) == col(recursive_cte.c.id)
            )
        )
        # TODO(@AmineDiro): Optimize get_knowledge_tree
        query = (
            select(KnowledgeDB)
            .join(recursive_cte, col(KnowledgeDB.id) == recursive_cte.c.id)
            .options(joinedload(KnowledgeDB.brains))
        )

        result = await self.session.exec(query)
        knowledge_list = result.unique().all()

        return list(knowledge_list)

    async def get_root_knowledge_user(self, user_id: UUID) -> list[KnowledgeDB]:
        query = (
            select(KnowledgeDB)
            .where(KnowledgeDB.parent_id.is_(None))  # type: ignore
            .where(KnowledgeDB.user_id == user_id)
            .options(joinedload(KnowledgeDB.children))  # type: ignore
        )
        result = await self.session.exec(query)
        kms = result.unique().all()
        return list(kms)

    async def get_knowledge_by_id(
        self, knowledge_id: UUID, user_id: UUID | None = None
    ) -> KnowledgeDB:
        query = (
            select(KnowledgeDB)
            .where(KnowledgeDB.id == knowledge_id)
            .options(joinedload(KnowledgeDB.parent), joinedload(KnowledgeDB.children))  # type: ignore
        )
        if user_id:
            query = query.where(KnowledgeDB.user_id == user_id)
        result = await self.session.exec(query)
        knowledge = result.first()
        if not knowledge:
            raise KnowledgeNotFoundException("Knowledge not found")
        return knowledge

    async def get_brain_by_id(
        self, brain_id: UUID, get_knowledge: bool = True
    ) -> Brain:
        query = select(Brain).where(Brain.brain_id == brain_id)
        if get_knowledge:
            query = query.options(
                joinedload(Brain.knowledges).joinedload(KnowledgeDB.brains)
            )
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
