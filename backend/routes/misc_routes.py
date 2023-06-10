from fastapi import APIRouter

misc_router = APIRouter()

@misc_router.get("/")
async def root():
    return {"status": "OK"}