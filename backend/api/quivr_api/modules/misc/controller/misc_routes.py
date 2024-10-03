from fastapi import APIRouter, Depends, HTTPException
from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import get_async_session
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

logger = get_logger(__name__)

misc_router = APIRouter()


@misc_router.get("/")
async def root():
    """
    Root endpoint to check the status of the API.
    """
    return {"status": "OK"}


@misc_router.get("/healthz", tags=["Health"])
async def healthz(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(text("SELECT 1"))
        if not result:
            raise HTTPException(status_code=500, detail="Database is not healthy")
    except Exception as e:
        logger.error(f"Error checking database health: {e}")
        raise HTTPException(status_code=500, detail="Database is not healthy")

    return {"status": "ok"}
