from typing import Annotated, List

from fastapi import APIRouter, Depends
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.models.entity.model import Model
from quivr_api.modules.models.service.model_service import ModelService
from quivr_api.modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)
model_router = APIRouter()

ModelServiceDep = Annotated[ModelService, Depends(get_service(ModelService))]
UserIdentityDep = Annotated[UserIdentity, Depends(get_current_user)]


# get all chats
@model_router.get(
    "/models",
    response_model=List[Model],
    dependencies=[Depends(AuthBearer())],
    tags=["Models"],
)
async def get_models(current_user: UserIdentityDep, model_service: ModelServiceDep):
    """
    Retrieve all models for the current user.
    """
    models = await model_service.get_models()
    return models
