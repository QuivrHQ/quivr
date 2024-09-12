from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.misc.service.misc_service import MiscService
from quivr_api.logger import get_logger

logger = get_logger(__name__)

misc_router = APIRouter()

MiscServiceDep = Annotated[MiscService, Depends(get_service(MiscService))]

@misc_router.get("/")
async def root():
    """
    Root endpoint to check the status of the API.
    """
    return {"status": "OK"}


@misc_router.get("/healthz", tags=["Health"])
async def healthz(misc_service: MiscServiceDep):
    
    try: 
        is_healthy = await misc_service.get_health()
    except Exception as e:
        logger.error(f"Error checking database health: {e}")
        raise HTTPException(status_code=500, detail="Database is not healthy")
    
    return {"status": "ok"}
