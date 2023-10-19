from uuid import UUID

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, HTTPException
from logger import get_logger
from models import UserIdentity, UserUsage
from models.brain_entity import PublicBrain
from models.databases.supabase.brains import (
    BrainQuestionRequest,
    BrainUpdatableProperties,
    CreateBrainProperties,
)
from repository.brain import (
    create_brain,
    create_brain_user,
    delete_brain_users,
    get_brain_details,
    get_default_user_brain_or_create_new,
    get_public_brains,
    get_question_context_from_brain,
    get_user_brains,
    get_user_default_brain,
    set_as_default_brain_for_user,
    update_brain_by_id,
)
from repository.prompt import delete_prompt_by_id, get_prompt_by_id
from routes.authorizations.brain_authorization import has_brain_authorization
from routes.authorizations.types import RoleEnum

logger = get_logger(__name__)
brain_router = APIRouter()


@brain_router.get("/brains/", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def retrieve_all_brains_for_user(
    current_user: UserIdentity = Depends(get_current_user),
):
    """Retrieve all brains for the current user."""
    brains = get_user_brains(current_user.id)
    return {"brains": brains}


@brain_router.get(
    "/brains/public", dependencies=[Depends(AuthBearer())], tags=["Brain"]
)
async def retrieve_public_brains() -> list[PublicBrain]:
    """Retrieve all Quivr public brains."""
    return get_public_brains()


@brain_router.get(
    "/brains/default/", dependencies=[Depends(AuthBearer())], tags=["Brain"]
)
async def retrieve_default_brain(
    current_user: UserIdentity = Depends(get_current_user),
):
    """Retrieve or create the default brain for the current user."""
    brain = get_default_user_brain_or_create_new(current_user)
    return {"id": brain.brain_id, "name": brain.name, "rights": "Owner"}


@brain_router.get(
    "/brains/{brain_id}/",
    dependencies=[Depends(AuthBearer()), Depends(has_brain_authorization())],
    tags=["Brain"],
)
async def retrieve_brain_by_id(brain_id: UUID):
    """Retrieve details of a specific brain by its ID."""
    brain_details = get_brain_details(brain_id)
    if brain_details is None:
        raise HTTPException(status_code=404, detail="Brain details not found")
    return brain_details


@brain_router.post("/brains/", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def create_new_brain(
    brain: CreateBrainProperties, current_user: UserIdentity = Depends(get_current_user)
):
    """Create a new brain for the user."""
    user_brains = get_user_brains(current_user.id)
    user_usage = UserUsage(
        id=current_user.id,
        email=current_user.email,
        openai_api_key=current_user.openai_api_key,
    )
    user_settings = user_usage.get_user_settings()

    if len(user_brains) >= user_settings.get("max_brains", 5):
        raise HTTPException(
            status_code=429,
            detail=f"Maximum number of brains reached ({user_settings.get('max_brains', 5)}).",
        )

    new_brain = create_brain(brain)
    if get_user_default_brain(current_user.id):
        logger.info(f"Default brain already exists for user {current_user.id}")
        create_brain_user(
            user_id=current_user.id,
            brain_id=new_brain.brain_id,
            rights=RoleEnum.Owner,
            is_default_brain=False,
        )
    else:
        logger.info(f"Creating default brain for user {current_user.id}.")
        create_brain_user(
            user_id=current_user.id,
            brain_id=new_brain.brain_id,
            rights=RoleEnum.Owner,
            is_default_brain=True,
        )

    return {"id": new_brain.brain_id, "name": brain.name, "rights": "Owner"}


@brain_router.put(
    "/brains/{brain_id}/",
    dependencies=[
        Depends(AuthBearer()),
        Depends(has_brain_authorization([RoleEnum.Editor, RoleEnum.Owner])),
    ],
    tags=["Brain"],
)
async def update_existing_brain(
    brain_id: UUID, brain_update_data: BrainUpdatableProperties
):
    """Update an existing brain's configuration."""
    existing_brain = get_brain_details(brain_id)
    if existing_brain is None:
        raise HTTPException(status_code=404, detail="Brain not found")

    if brain_update_data.prompt_id is None and existing_brain.prompt_id:
        prompt = get_prompt_by_id(existing_brain.prompt_id)
        if prompt and prompt.status == "private":
            delete_prompt_by_id(existing_brain.prompt_id)

    if brain_update_data.status == "private" and existing_brain.status == "public":
        delete_brain_users(brain_id)

    update_brain_by_id(brain_id, brain_update_data)
    return {"message": f"Brain {brain_id} has been updated."}


@brain_router.post(
    "/brains/{brain_id}/default",
    dependencies=[Depends(AuthBearer()), Depends(has_brain_authorization())],
    tags=["Brain"],
)
async def set_brain_as_default(
    brain_id: UUID, user: UserIdentity = Depends(get_current_user)
):
    """Set a brain as the default for the current user."""
    set_as_default_brain_for_user(user.id, brain_id)
    return {"message": f"Brain {brain_id} has been set as default brain."}


@brain_router.post(
    "/brains/{brain_id}/question_context",
    dependencies=[Depends(AuthBearer()), Depends(has_brain_authorization())],
    tags=["Brain"],
)
async def get_question_context_for_brain(brain_id: UUID, request: BrainQuestionRequest):
    """Retrieve the question context from a specific brain."""
    context = get_question_context_from_brain(brain_id, request.question)
    return {"context": context}
