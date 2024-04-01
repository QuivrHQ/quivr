from uuid import UUID
from fastapi import APIRouter, Depends
from middlewares.auth.auth_bearer import AuthBearer, get_current_user
from modules.analytics.service.analytics_service import AnalyticsService

analytics_service = AnalyticsService()
analytics_router = APIRouter()

@analytics_router.get(
    "/analytics/brains-usages", dependencies=[Depends(AuthBearer())], tags=["Analytics"]
)
async def get_brains_usages(
    user_id: UUID = Depends(get_current_user).id,
):
    """
    Get all user brains usages
    """

    return analytics_service.get_brains_usages(user_id)
