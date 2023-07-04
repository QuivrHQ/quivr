from fastapi import APIRouter

misc_router = APIRouter()


@misc_router.get("/")
async def root():
    """
    Root endpoint to check the status of the API.
    """
    return {"status": "OK"}
