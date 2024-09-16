from http import HTTPStatus
from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.brain.entity.brain_entity import RoleEnum
from quivr_api.modules.brain.service.brain_authorization_service import (
    has_brain_authorization,
    validate_brain_authorization,
)
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.knowledge.dto.inputs import AddKnowledge
from quivr_api.modules.knowledge.entity.knowledge import Knowledge, KnowledgeUpdate
from quivr_api.modules.knowledge.service.knowledge_exceptions import (
    KnowledgeDeleteError,
    KnowledgeForbiddenAccess,
    KnowledgeNotFoundException,
    UploadError,
)
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.upload.service.generate_file_signed_url import (
    generate_file_signed_url,
)
from quivr_api.modules.user.entity.user_identity import UserIdentity

knowledge_router = APIRouter()
logger = get_logger(__name__)

get_km_service = get_service(KnowledgeService)
KnowledgeServiceDep = Annotated[KnowledgeService, Depends(get_km_service)]


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
async def delete_knowledge_brain(
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
    await knowledge_service.remove_knowledge_brain(brain_id, knowledge_id)

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

    if len(knowledge.brains) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="knowledge not associated with brains yet.",
        )

    brain_id = knowledge.brains[0]["brain_id"]

    validate_brain_authorization(brain_id=brain_id, user_id=current_user.id)

    if knowledge.file_name is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Knowledge with id {knowledge_id} is not a file.",
        )

    file_path_in_storage = f"{brain_id}/{knowledge.file_name}"
    file_signed_url = generate_file_signed_url(file_path_in_storage)

    return file_signed_url


@knowledge_router.post(
    "/knowledge/",
    tags=["Knowledge"],
    response_model=Knowledge,
)
async def create_knowledge(
    knowledge_data: str = File(...),
    file: Optional[UploadFile] = None,
    knowledge_service: KnowledgeService = Depends(get_km_service),
    current_user: UserIdentity = Depends(get_current_user),
):
    knowledge = AddKnowledge.model_validate_json(knowledge_data)
    if not knowledge.file_name and not knowledge.url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either file_name or url must be provided",
        )
    try:
        km = await knowledge_service.create_knowledge(
            knowledge_to_add=knowledge, upload_file=file, user_id=current_user.id
        )
        km_dto = await km.to_dto()
        return km_dto
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable knowledge ",
        )
    except FileExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Existing knowledge"
        )
    except UploadError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occured uploading knowledge",
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@knowledge_router.get(
    "/knowledge/children",
    response_model=List[Knowledge] | None,
    tags=["Knowledge"],
)
async def list_knowledge(
    parent_id: UUID | None = None,
    knowledge_service: KnowledgeService = Depends(get_km_service),
    current_user: UserIdentity = Depends(get_current_user),
):
    try:
        # TODO: Returns one level of children
        children = await knowledge_service.list_knowledge(parent_id, current_user.id)
        return [await c.to_dto(get_children=False) for c in children]
    except KnowledgeNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"{e.message}"
        )
    except KnowledgeForbiddenAccess as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{e.message}"
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@knowledge_router.get(
    "/knowledge/{knowledge_id}",
    response_model=Knowledge,
    tags=["Knowledge"],
)
async def get_knowledge(
    knowledge_id: UUID,
    knowledge_service: KnowledgeService = Depends(get_km_service),
    current_user: UserIdentity = Depends(get_current_user),
):
    try:
        km = await knowledge_service.get_knowledge(knowledge_id)
        if km.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this knowledge.",
            )
        return await km.to_dto()
    except KnowledgeNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{e.message}"
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@knowledge_router.patch(
    "/knowledge/{knowledge_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Knowledge,
    tags=["Knowledge"],
)
async def update_knowledge(
    knowledge_id: UUID,
    payload: KnowledgeUpdate,
    knowledge_service: KnowledgeService = Depends(get_km_service),
    current_user: UserIdentity = Depends(get_current_user),
):
    try:
        km = await knowledge_service.get_knowledge(knowledge_id)
        if km.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this knowledge.",
            )
        km = await knowledge_service.update_knowledge(km, payload)
        return km
    except KnowledgeNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{e.message}"
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@knowledge_router.delete(
    "/knowledge/{knowledge_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Knowledge"],
)
async def delete_knowledge(
    knowledge_id: UUID,
    knowledge_service: KnowledgeService = Depends(get_km_service),
    current_user: UserIdentity = Depends(get_current_user),
):
    try:
        km = await knowledge_service.get_knowledge(knowledge_id)

        if km.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to remove this knowledge.",
            )
        delete_response = await knowledge_service.remove_knowledge(km)
        return delete_response
    except KnowledgeNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{e.message}"
        )
    except KnowledgeDeleteError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
