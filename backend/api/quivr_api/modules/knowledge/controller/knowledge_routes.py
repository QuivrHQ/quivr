import asyncio
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from quivr_core.models import KnowledgeStatus

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.brain.entity.brain_entity import RoleEnum
from quivr_api.modules.brain.service.brain_authorization_service import (
    has_brain_authorization,
    validate_brain_authorization,
)
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.knowledge.dto.inputs import (
    AddKnowledge,
    KnowledgeUpdate,
    LinkKnowledgeBrain,
    UnlinkKnowledgeBrain,
)
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_api.modules.knowledge.service.knowledge_exceptions import (
    KnowledgeDeleteError,
    KnowledgeForbiddenAccess,
    KnowledgeNotFoundException,
    UploadError,
)
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.dto.inputs import CreateNotification
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.upload.service.generate_file_signed_url import (
    generate_file_signed_url,
)
from quivr_api.modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)
knowledge_router = APIRouter()

notification_service = NotificationService()
get_knowledge_service = get_service(KnowledgeService)
get_sync_service = get_service(SyncsService)


@knowledge_router.get(
    "/knowledge", dependencies=[Depends(AuthBearer())], tags=["Knowledge"]
)
async def list_knowledge_in_brain_endpoint(
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
    brain_id: UUID = Query(..., description="The ID of the brain"),
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Retrieve and list all the knowledge in a brain.
    """
    validate_brain_authorization(brain_id=brain_id, user_id=current_user.id)

    knowledges = await knowledge_service.get_all_knowledge_in_brain(brain_id)

    return {"knowledges": knowledges}


@knowledge_router.get(
    "/knowledge/{knowledge_id}/signed_download_url",
    dependencies=[Depends(AuthBearer())],
    tags=["Knowledge"],
)
async def generate_signed_url_endpoint(
    knowledge_id: UUID,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
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
    response_model=KnowledgeDTO,
)
async def create_knowledge(
    knowledge_data: str = File(...),
    file: Optional[UploadFile] = None,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
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
    "/knowledge/files",
    response_model=List[KnowledgeDTO] | None,
    tags=["Knowledge"],
)
async def list_knowledge(
    parent_id: UUID | None = None,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
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
    response_model=KnowledgeDTO,
    tags=["Knowledge"],
)
async def get_knowledge(
    knowledge_id: UUID,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
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
    response_model=KnowledgeDTO,
    tags=["Knowledge"],
)
async def update_knowledge(
    knowledge_id: UUID,
    payload: KnowledgeUpdate,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
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
    dependencies=[
        Depends(AuthBearer()),
        Depends(has_brain_authorization(RoleEnum.Owner)),
    ],
    tags=["Knowledge"],
)
async def delete_knowledge_brain(
    knowledge_id: UUID,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
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


@knowledge_router.delete(
    "/knowledge/{knowledge_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Knowledge"],
)
async def delete_knowledge(
    knowledge_id: UUID,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
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


@knowledge_router.post(
    "/knowledge/link_to_brains/",
    status_code=status.HTTP_201_CREATED,
    response_model=List[KnowledgeDTO],
    tags=["Knowledge"],
)
async def link_knowledge_to_brain(
    link_request: LinkKnowledgeBrain,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
    current_user: UserIdentity = Depends(get_current_user),
):
    brains_ids, knowledge_dto, bulk_id = (
        link_request.brain_ids,
        link_request.knowledge,
        link_request.bulk_id,
    )
    if len(brains_ids) == 0:
        return "empty brain list"

    if knowledge_dto.id is None:
        if knowledge_dto.sync_file_id is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unknown knowledge entity"
            )
        # Create a knowledge from this sync
        knowledge = await knowledge_service.create_knowledge(
            user_id=current_user.id,
            knowledge_to_add=AddKnowledge(**knowledge_dto.model_dump()),
            upload_file=None,
        )
        linked_kms = await knowledge_service.link_knowledge_tree_brains(
            knowledge, brains_ids=brains_ids, user_id=current_user.id
        )

    else:
        linked_kms = await knowledge_service.link_knowledge_tree_brains(
            knowledge_dto.id, brains_ids=brains_ids, user_id=current_user.id
        )

    for knowledge in filter(
        lambda k: k.status
        not in [KnowledgeStatus.PROCESSED, KnowledgeStatus.PROCESSING],
        linked_kms,
    ):
        assert knowledge.id
        upload_notification = notification_service.add_notification(
            CreateNotification(
                user_id=current_user.id,
                bulk_id=bulk_id,
                status=NotificationsStatusEnum.INFO,
                title=f"{knowledge.file_name}",
                category="process",
            )
        )
        celery.send_task(
            "process_file_task",
            kwargs={
                "knowledge_id": knowledge.id,
                "notification_id": upload_notification.id,
            },
        )
        knowledge = await knowledge_service.update_knowledge(
            knowledge=knowledge,
            payload=KnowledgeUpdate(status=KnowledgeStatus.PROCESSING),
        )

    return await asyncio.gather(*[k.to_dto() for k in linked_kms])


@knowledge_router.delete(
    "/knowledge/unlink_from_brains/",
    response_model=List[KnowledgeDTO] | None,
    tags=["Knowledge"],
)
async def unlink_knowledge_from_brain(
    unlink_request: UnlinkKnowledgeBrain,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
    current_user: UserIdentity = Depends(get_current_user),
):
    brains_ids, knowledge_id = unlink_request.brain_ids, unlink_request.knowledge_id

    if len(brains_ids) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
        )

    km = await knowledge_service.get_knowledge(knowledge_id)
    if km.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to remove this knowledge.",
        )

    unlinked_kms = await knowledge_service.unlink_knowledge_tree_brains(
        knowledge=knowledge_id, brains_ids=brains_ids, user_id=current_user.id
    )

    if unlinked_kms:
        return await asyncio.gather(*[k.to_dto() for k in unlinked_kms])
