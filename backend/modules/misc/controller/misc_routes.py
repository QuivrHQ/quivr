from fastapi import APIRouter

misc_router = APIRouter()


@misc_router.get("/")
async def root():
    """
    Root endpoint to check the status of the API.
    """
    return {"status": "OK"}


@misc_router.get("/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}
