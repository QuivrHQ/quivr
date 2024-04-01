from uuid import UUID
from fastapi import APIRouter, Depends, Query
from middlewares.auth.auth_bearer import AuthBearer
from modules.analytics.service.analytics_service import AnalyticsService

analytics_service = AnalyticsService()
analytics_router = APIRouter()

@analytics_router.get(
    "/analytics/brains_usages", dependencies=[Depends(AuthBearer())], tags=["Analytics"]
)
async def get_brains_usages(
    user_id: UUID = Query(..., description="The ID of the user"),
):
    """
    Get all user brains usages
    """

    return analytics_service.get_brains_usages(user_id)
