from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from quivr_core.api.modules.dependencies import get_service
from quivr_core.api.modules.prompt.entity.prompt import (
    CreatePromptProperties,
    Prompt,
    PromptUpdatableProperties,
)
from quivr_core.api.modules.prompt.service import PromptService

prompt_router = APIRouter()


PromptServiceDep = Annotated[PromptService, Depends(get_service(PromptService))]


@prompt_router.get("/prompts", tags=["Prompt"])
async def get_prompts(
    prompt_service: PromptServiceDep,
) -> list[Prompt]:
    """
    Retrieve all public prompt
    """
    return prompt_service.get_public_prompts()


@prompt_router.get("/prompts/{prompt_id}", tags=["Prompt"])
async def get_prompt(
    prompt_id: UUID,
    prompt_service: PromptServiceDep,
) -> Prompt | None:
    """
    Retrieve a prompt by its id
    """

    return prompt_service.get_prompt_by_id(prompt_id)


@prompt_router.put("/prompts/{prompt_id}", tags=["Prompt"])
async def update_prompt(
    prompt_id: UUID,
    prompt: PromptUpdatableProperties,
    prompt_service: PromptServiceDep,
) -> Prompt | None:
    """
    Update a prompt by its id
    """

    return prompt_service.update_prompt_by_id(prompt_id, prompt)


@prompt_router.post("/prompts", tags=["Prompt"])
async def create_prompt_route(
    prompt: CreatePromptProperties,
    prompt_service: PromptServiceDep,
) -> Prompt | None:
    """
    Create a prompt by its id
    """

    return prompt_service.create_prompt(prompt)
