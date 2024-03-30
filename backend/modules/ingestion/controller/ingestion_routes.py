from typing import List

from fastapi import APIRouter, Depends
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.ingestion.entity.ingestion import IngestionEntity
from modules.ingestion.service.ingestion import Ingestion
from modules.user.entity.user_identity import UserIdentity

ingestion_router = APIRouter()
logger = get_logger(__name__)

ingestion_service = Ingestion()


@ingestion_router.get(
    "/ingestion", dependencies=[Depends(AuthBearer())], tags=["Ingestion"]
)
async def list_ingestion(
    current_user: UserIdentity = Depends(get_current_user),
) -> List[IngestionEntity]:
    """
    Retrieve and list all the knowledge in a brain.
    """

    ingestions = ingestion_service.get_all_ingestions()
    return ingestions
