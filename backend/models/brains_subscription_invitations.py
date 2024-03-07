from uuid import UUID

from logger import get_logger
from pydantic import ConfigDict, BaseModel

logger = get_logger(__name__)


class BrainSubscription(BaseModel):
    brain_id: UUID
    email: str
    rights: str = "Viewer"
    model_config = ConfigDict(arbitrary_types_allowed=True)
