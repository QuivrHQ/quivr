from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth.auth_bearer import AuthBearer, get_current_user
from quivr_api.modules.brain.dto.inputs import (
    BrainQuestionRequest,
    BrainUpdatableProperties,
    CreateBrainProperties,
)
from quivr_api.modules.brain.entity.brain_entity import (
    BrainType,
    MinimalUserBrainEntity,
    RoleEnum,
)
from quivr_api.modules.brain.entity.integration_brain import (
    IntegrationDescriptionEntity,
)
from quivr_api.modules.brain.service.brain_authorization_service import (
    has_brain_authorization,
)
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_user_service import BrainUserService
from quivr_api.modules.brain.service.get_question_context_from_brain import (
    get_question_context_from_brain,
)
from quivr_api.modules.brain.service.integration_brain_service import (
    IntegrationBrainDescriptionService,
)
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.models.service.model_service import ModelService
from quivr_api.modules.prompt.service.prompt_service import PromptService
from quivr_api.modules.user.entity.user_identity import UserIdentity
from quivr_api.modules.user.service.user_usage import UserUsage
from quivr_api.packages.utils.telemetry import maybe_send_telemetry
from quivr_api.packages.utils.uuid_generator import generate_uuid_from_string

logger = get_logger(__name__)
brain_router = APIRouter()

prompt_service = PromptService()
brain_service = BrainService()
brain_user_service = BrainUserService()
integration_brain_description_service = IntegrationBrainDescriptionService()
ModelServiceDep = Annotated[ModelService, Depends(get_service(ModelService))]


@brain_router.get(
    "/brains/integrations/",
    dependencies=[Depends(AuthBearer())],
)
async def get_integration_brain_description() -> list[IntegrationDescriptionEntity]:
    """Retrieve the integration brain description."""
    # TODO: Deprecated, remove this endpoint
    return []


@brain_router.get("/brains/", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def retrieve_all_brains_for_user(
    model_service: ModelServiceDep,
    current_user: UserIdentity = Depends(get_current_user),
):
    """Retrieve all brains for the current user."""
    brains = brain_user_service.get_user_brains(current_user.id)
    models = await model_service.get_models()
    default_model = await model_service.get_default_model()

    for brain in brains:
        # find the brain.model in models and set the brain.price to the model.price
        found = False
        if brain.model:
            for model in models:
                if model.name == brain.model:
                    brain.price = model.price
                    found = True
                    break
        if not found:
            brain.price = default_model.price

    for model in models:
        brains.append(
            MinimalUserBrainEntity(
                id=generate_uuid_from_string(model.name),
                status="private",
                brain_type=BrainType.model,
                name=model.name,
                rights=RoleEnum.Viewer,
                model=True,
                price=model.price,
                max_input=model.max_input,
                max_output=model.max_output,
                display_name=model.display_name,
                image_url=model.image_url,
                description=model.description,
                integration_logo_url="model.integration_id",
                max_files=0,
            )
        )

    return {"brains": brains}


@brain_router.get(
    "/brains/{brain_id}/",
    dependencies=[
        Depends(AuthBearer()),
        Depends(
            has_brain_authorization(
                required_roles=[RoleEnum.Owner, RoleEnum.Editor, RoleEnum.Viewer]
            )
        ),
    ],
    tags=["Brain"],
)
async def retrieve_brain_by_id(
    brain_id: UUID,
    current_user: UserIdentity = Depends(get_current_user),
):
    """Retrieve details of a specific brain by its ID."""
    brain_details = brain_service.get_brain_details(brain_id, current_user.id)
    if brain_details is None:
        raise HTTPException(status_code=404, detail="Brain details not found")
    return brain_details


@brain_router.post("/brains/", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def create_new_brain(
    brain: CreateBrainProperties,
    request: Request,
    current_user: UserIdentity = Depends(get_current_user),
):
    """Create a new brain for the user."""
    user_brains = brain_user_service.get_user_brains(current_user.id)
    user_usage = UserUsage(
        id=current_user.id,
        email=current_user.email,
    )
    user_settings = user_usage.get_user_settings()

    if len(user_brains) >= user_settings.get("max_brains", 5):
        raise HTTPException(
            status_code=429,
            detail=f"Maximum number of brains reached ({user_settings.get('max_brains', 5)}).",
        )
    maybe_send_telemetry("create_brain", {"brain_name": brain.name}, request)
    new_brain = brain_service.create_brain(
        brain=brain,
        user_id=current_user.id,
    )
    brain_user_service.create_brain_user(
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
    brain_id: UUID,
    brain_update_data: BrainUpdatableProperties,
    current_user: UserIdentity = Depends(get_current_user),
):
    """Update an existing brain's configuration."""
    existing_brain = brain_service.get_brain_details(brain_id, current_user.id)
    if existing_brain is None:
        raise HTTPException(status_code=404, detail="Brain not found")

    if brain_update_data.prompt_id is None and existing_brain.prompt_id:
        prompt = prompt_service.get_prompt_by_id(existing_brain.prompt_id)
        if prompt and prompt.status == "private":
            prompt_service.delete_prompt_by_id(existing_brain.prompt_id)

            return {"message": f"Prompt {brain_id} has been updated."}

    elif brain_update_data.status == "private" and existing_brain.status == "public":
        brain_user_service.delete_brain_users(brain_id)
        return {"message": f"Brain {brain_id} has been deleted."}

    else:
        brain_service.update_brain_by_id(brain_id, brain_update_data)

        return {"message": f"Brain {brain_id} has been updated."}


@brain_router.post(
    "/brains/{brain_id}/documents",
    dependencies=[Depends(AuthBearer()), Depends(has_brain_authorization())],
    tags=["Brain"],
)
async def get_question_context_for_brain(
    brain_id: UUID, question: BrainQuestionRequest
):
    # TODO: Move this endpoint to AnswerGenerator service
    """Retrieve the question context from a specific brain."""
    context = get_question_context_from_brain(brain_id, question.question)
    return {"docs": context}
