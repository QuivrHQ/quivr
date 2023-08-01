from auth import AuthBearer
from fastapi import APIRouter, Depends
from models.prompt import Prompt
from repository.prompt.get_public_prompts import get_public_prompts

prompt_router = APIRouter()


@prompt_router.get("/prompts", dependencies=[Depends(AuthBearer())], tags=["Prompt"])
async def get_prompts() -> list[Prompt]:
    """
    Retrieve all public prompt
    """

    return get_public_prompts()
