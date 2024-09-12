
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.dependencies import BaseRepository


class MiscRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)


    async def get_health(self) -> bool:
        """
        Check if the database is healthy by executing a simple query.
        """
        query = select(1)
        response = await self.session.exec(query)
        
        # Check if the response is just 1
        return response.all() == [1]
