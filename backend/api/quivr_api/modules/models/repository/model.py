from typing import Sequence

from quivr_api.modules.dependencies import BaseRepository, get_supabase_client
from quivr_api.modules.models.entity.model import Model
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class ModelRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        # TODO: for now use it instead of session
        self.db = get_supabase_client()

    async def get_models(self) -> Sequence[Model]:
        query = select(Model)
        response = await self.session.exec(query)
        return response.all()

    async def get_model(self, model_name: str) -> Model | None:
        query = select(Model).where(Model.name == model_name)
        response = await self.session.exec(query)
        return response.first()

    async def get_default_model(self) -> Model:
        query = select(Model).where(Model.default == True)  # noqa: E712
        response = await self.session.exec(query)
        return response.first()
