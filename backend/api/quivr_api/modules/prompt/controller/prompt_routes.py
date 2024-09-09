from uuid import UUID

from fastapi import APIRouter, Depends
from quivr_api.middlewares.auth import AuthBearer
from quivr_api.modules.prompt.entity.prompt import (
    CreatePromptProperties,
    Prompt,
    PromptUpdatableProperties,
)
from quivr_api.modules.prompt.service import PromptService

prompt_router = APIRouter()

promptService = PromptService()


@prompt_router.get("/prompts", dependencies=[Depends(AuthBearer())], tags=["Prompt"])
async def get_prompts() -> list[Prompt]:
    """
    Retrieve all public prompt
    """
    return promptService.get_public_prompts()


@prompt_router.get(
    "/prompts/{prompt_id}", dependencies=[Depends(AuthBearer())], tags=["Prompt"]
)
async def get_prompt(prompt_id: UUID) -> Prompt | None:
    """
    Retrieve a prompt by its id
    """

    return promptService.get_prompt_by_id(prompt_id)


@prompt_router.put(
    "/prompts/{prompt_id}", dependencies=[Depends(AuthBearer())], tags=["Prompt"]
)
async def update_prompt(
    prompt_id: UUID, prompt: PromptUpdatableProperties
) -> Prompt | None:
    """
    Update a prompt by its id
    """

    return promptService.update_prompt_by_id(prompt_id, prompt)


@prompt_router.post("/prompts", dependencies=[Depends(AuthBearer())], tags=["Prompt"])
async def create_prompt_route(prompt: CreatePromptProperties) -> Prompt | None:
    """
    Create a prompt by its id
    """

    return promptService.create_prompt(prompt)
