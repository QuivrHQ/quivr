from uuid import UUID

from fastapi import APIRouter, Depends, Query

from backend.middlewares.auth.auth_bearer import AuthBearer, get_current_user
from backend.modules.analytics.entity.analytics import Range
from backend.modules.analytics.service.analytics_service import AnalyticsService

analytics_service = AnalyticsService()
analytics_router = APIRouter()


@analytics_router.get(
    "/analytics/brains-usages", dependencies=[Depends(AuthBearer())], tags=["Analytics"]
)
async def get_brains_usages(
    user: UUID = Depends(get_current_user),
    brain_id: UUID = Query(None),
    graph_range: Range = Query(Range.WEEK, alias="graph_range"),
):
    """
    Get all user brains usages
    """

    return analytics_service.get_brains_usages(user.id, graph_range, brain_id)
