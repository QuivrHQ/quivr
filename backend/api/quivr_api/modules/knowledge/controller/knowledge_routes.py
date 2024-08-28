from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.brain.entity.brain_entity import RoleEnum
from quivr_api.modules.brain.service.brain_authorization_service import (
    has_brain_authorization,
    validate_brain_authorization,
)
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.upload.service.generate_file_signed_url import (
    generate_file_signed_url,
)
from quivr_api.modules.user.entity.user_identity import UserIdentity

knowledge_router = APIRouter()
logger = get_logger(__name__)

KnowledgeServiceDep = Annotated[
    KnowledgeService, Depends(get_service(KnowledgeService))
]


@knowledge_router.get(
    "/knowledge", dependencies=[Depends(AuthBearer())], tags=["Knowledge"]
)
async def list_knowledge_in_brain_endpoint(
    knowledge_service: KnowledgeServiceDep,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Retrieve and list all the knowledge in a brain.
    """

    validate_brain_authorization(brain_id=brain_id, user_id=current_user.id)

    knowledges = await knowledge_service.get_all_knowledge_in_brain(brain_id)

    return {"knowledges": knowledges}


@knowledge_router.delete(
    "/knowledge/{knowledge_id}",
    dependencies=[
        Depends(AuthBearer()),
        Depends(has_brain_authorization(RoleEnum.Owner)),
    ],
    tags=["Knowledge"],
)
async def delete_endpoint(
    knowledge_id: UUID,
    knowledge_service: KnowledgeServiceDep,
    current_user: UserIdentity = Depends(get_current_user),
    brain_id: UUID = Query(..., description="The ID of the brain"),
):
    """
    Delete a specific knowledge from a brain.
    """

    knowledge = await knowledge_service.get_knowledge(knowledge_id)
    file_name = knowledge.file_name if knowledge.file_name else knowledge.url
    await knowledge_service.remove_knowledge(brain_id, knowledge_id)

    brain_vector_service = BrainVectorService(brain_id)
    if knowledge.file_name:
        brain_vector_service.delete_file_from_brain(knowledge.file_name)
    elif knowledge.url:
        brain_vector_service.delete_file_url_from_brain(knowledge.url)

    return {
        "message": f"{file_name} of brain {brain_id} has been deleted by user {current_user.email}."
    }


@knowledge_router.get(
    "/knowledge/{knowledge_id}/signed_download_url",
    dependencies=[Depends(AuthBearer())],
    tags=["Knowledge"],
)
async def generate_signed_url_endpoint(
    knowledge_id: UUID,
    knowledge_service: KnowledgeServiceDep,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Generate a signed url to download the file from storage.
    """

    knowledge = await knowledge_service.get_knowledge(knowledge_id)

    if len(knowledge.brains_ids) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="knowledge not associated with brains yet.",
        )

    brain_id = knowledge.brains_ids[0]

    validate_brain_authorization(brain_id=brain_id, user_id=current_user.id)

    if knowledge.file_name is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Knowledge with id {knowledge_id} is not a file.",
        )

    file_path_in_storage = f"{brain_id}/{knowledge.file_name}"
    file_signed_url = generate_file_signed_url(file_path_in_storage)

    return file_signed_url
