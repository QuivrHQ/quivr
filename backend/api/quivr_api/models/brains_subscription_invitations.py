from uuid import UUID

from pydantic import BaseModel, ConfigDict
from quivr_api.logger import get_logger

logger = get_logger(__name__)


class BrainSubscription(BaseModel):
    brain_id: UUID
    email: str
    rights: str = "Viewer"
    model_config = ConfigDict(arbitrary_types_allowed=True)
