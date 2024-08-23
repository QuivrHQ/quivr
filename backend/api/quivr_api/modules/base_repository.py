from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from quivr_api.modules.base_uuid_entity import BaseUUIDModel
from sqlalchemy import exc
from sqlmodel import SQLModel, col, select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=BaseUUIDModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class BaseCRUDRepository(Generic[ModelType, CreateSchema, UpdateSchema]):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        """
        Base repository for default CRUD operations
        """
        self.model = model
        self.session = session

    def get_db(self) -> AsyncSession:
        return self.session

    async def get_by_id(
        self, *, id: UUID, db_session: AsyncSession
    ) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        response = await db_session.exec(query)
        return response.one()

    async def get_by_ids(
        self,
        *,
        list_ids: list[UUID],
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType] | None:
        db_session = db_session or self.session
        response = await db_session.exec(
            select(self.model).where(col(self.model.id).in_(list_ids))
        )
        return response.all()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        db_session = db_session or self.session
        query = select(self.model).offset(skip).limit(limit)
        response = await db_session.exec(query)
        return response.all()

    async def create(
        self,
        *,
        entity: CreateSchema | ModelType,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        db_session = db_session or self.session
        db_obj = self.model.model_validate(entity)  # type: ignore

        try:
            db_session.add(db_obj)
            await db_session.commit()
        except exc.IntegrityError:
            await db_session.rollback()
            # TODO(@aminediro) : for now, build an exception system
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        await db_session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchema | dict[str, Any] | ModelType,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        db_session = db_session or self.session

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)
        return obj_current

    async def remove(
        self, *, id: UUID | str, db_session: AsyncSession | None = None
    ) -> ModelType:
        db_session = db_session or self.session
        response = await db_session.exec(select(self.model).where(self.model.id == id))
        obj = response.one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj
