

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.misc.repository.misc import MiscRepository

logger = get_logger(__name__)



class MiscService(BaseService[MiscRepository]):
    repository_cls = MiscRepository

    def __init__(self, repository: MiscRepository):
        self.repository = repository

    async def get_health(self) -> bool:
        return await self.repository.get_health()