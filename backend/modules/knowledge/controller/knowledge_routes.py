from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.brain.entity.brain_entity import RoleEnum
from modules.brain.service.brain_authorization_service import (
    has_brain_authorization,
    validate_brain_authorization,
)
from modules.brain.service.brain_vector_service import BrainVectorService
from modules.knowledge.service.knowledge_service import KnowledgeService
from modules.user.entity.user_identity import UserIdentity
from repository.files.generate_file_signed_url import generate_file_signed_url

knowledge_router = APIRouter()
logger = get_logger(__name__)

knowledge_service = KnowledgeService()


@knowledge_router.get(
    "/knowledge", dependencies=[Depends(AuthBearer())], tags=["Knowledge"]
)
async def list_knowledge_in_brain_endpoint(
    brain_id: UUID = Query(..., description="The ID of the brain"),
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Retrieve and list all the knowledge in a brain.
    """

    validate_brain_authorization(brain_id=brain_id, user_id=current_user.id)

    knowledges = knowledge_service.get_all_knowledge(brain_id)

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
    current_user: UserIdentity = Depends(get_current_user),
    brain_id: UUID = Query(..., description="The ID of the brain"),
):
    """
    Delete a specific knowledge from a brain.
    """

    knowledge = knowledge_service.get_knowledge(knowledge_id)
    file_name = knowledge.file_name if knowledge.file_name else knowledge.url
    knowledge_service.remove_knowledge(knowledge_id)

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
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Generate a signed url to download the file from storage.
    """

    knowledge = knowledge_service.get_knowledge(knowledge_id)

    validate_brain_authorization(brain_id=knowledge.brain_id, user_id=current_user.id)

    if knowledge.file_name == None:
        raise HTTPException(
            status_code=404,
            detail=f"Knowledge with id {knowledge_id} is not a file.",
        )

    file_path_in_storage = f"{knowledge.brain_id}/{knowledge.file_name}"

    file_signed_url = generate_file_signed_url(file_path_in_storage)

    return file_signed_url
