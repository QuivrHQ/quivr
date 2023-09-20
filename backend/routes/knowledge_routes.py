from uuid import UUID

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Query
from logger import get_logger
from models import Brain, UserIdentity, get_supabase_db
from repository.files.delete_file import delete_file_from_storage
from repository.files.generate_file_signed_url import generate_file_signed_url
from repository.knowledge.get_all_knowledge import get_all_knowledge
from repository.knowledge.get_knowledge import get_knowledge
from repository.knowledge.remove_knowledge import remove_knowledge
from routes.authorizations.brain_authorization import (
    RoleEnum,
    has_brain_authorization,
    validate_brain_authorization,
)

knowledge_router = APIRouter()
logger = get_logger(__name__)


@knowledge_router.get(
    "/knowledge/", dependencies=[Depends(AuthBearer())], tags=["Knowledge"]
)
async def list_knowledge_in_brain_endpoint(
    brain_id: UUID = Query(..., description="The ID of the brain"),
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Retrieve and list all the knowledge in a brain.
    """

    validate_brain_authorization(brain_id=brain_id, user_id=current_user.id)

    brain = Brain(id=brain_id)

    # files = list_files_from_storage(str(brain_id))
    # logger.info("List of files from storage", files)

    knowledges = get_all_knowledge(brain_id)
    logger.info("List of knowledge from knowledge table", knowledges)
    # TO DO: Retrieve from Knowledge table instead of storage or vectors
    unique_data = brain.get_unique_brain_files()

    print("UNIQUE DATA", unique_data)
    unique_data.sort(key=lambda x: int(x["size"]), reverse=True)

    return {"knowledges": knowledges}


@knowledge_router.delete(
    "/knowledge/{knowledge_id}/",
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

    validate_brain_authorization(brain_id=brain_id, user_id=current_user.id)

    brain = Brain(id=brain_id)

    knowledge = get_knowledge(knowledge_id)
    file_name = knowledge.file_name if knowledge.file_name else knowledge.url
    message = remove_knowledge(knowledge_id)

    print("MESSAGE to remove", message)
    if knowledge.file_name:
        delete_file_from_storage(f"{brain_id}/{knowledge.file_name}")
        brain.delete_file_from_brain(knowledge.file_name)
    elif knowledge.url:
        brain.delete_file_from_brain(knowledge.url)

    return {
        "message": f"{file_name} of brain {brain_id} has been deleted by user {current_user.email}."
    }


@knowledge_router.get(
    "/explore/{file_name}/signed_download_url",
    dependencies=[Depends(AuthBearer())],
    tags=["Knowledge"],
)
async def generate_signed_url_endpoint(
    file_name: str, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Generate a signed url to download the file from storage.
    """
    # check if user has the right to get the file: add brain_id to the query

    supabase_db = get_supabase_db()
    response = supabase_db.get_vectors_by_file_name(file_name)
    documents = response.data

    if len(documents) == 0:
        return {"documents": []}

    related_brain_id = (
        documents[0]["brains_vectors"][0]["brain_id"]
        if len(documents[0]["brains_vectors"]) != 0
        else None
    )
    if related_brain_id is None:
        raise Exception(f"File {file_name} has no brain_id associated with it")

    file_path_in_storage = f"{related_brain_id}/{file_name}"

    print("FILE PATH IN STORAGE", file_path_in_storage)
    file_signed_url = generate_file_signed_url(file_path_in_storage)

    print("FILE SIGNED URL", file_signed_url)

    validate_brain_authorization(brain_id=related_brain_id, user_id=current_user.id)

    return file_signed_url
