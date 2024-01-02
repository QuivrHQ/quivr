from uuid import UUID

from logger import get_logger
from models.settings import get_supabase_client
from modules.brain.entity.composite_brain_connection_entity import (
    CompositeBrainConnectionEntity,
)
from modules.brain.repository.interfaces import CompositeBrainsConnectionsInterface

logger = get_logger(__name__)


class CompositeBrainsConnections(CompositeBrainsConnectionsInterface):
    def __init__(self):
        self.db = get_supabase_client()

    def connect_brain(
        self, composite_brain_id: UUID, connected_brain_id: UUID
    ) -> CompositeBrainConnectionEntity:
        response = (
            self.db.table("composite_brain_connections")
            .insert(
                {
                    "composite_brain_id": str(composite_brain_id),
                    "connected_brain_id": str(connected_brain_id),
                }
            )
            .execute()
        )

        return CompositeBrainConnectionEntity(**response.data[0])

    def get_connected_brains(self, composite_brain_id: UUID) -> list[UUID]:
        response = (
            self.db.from_("composite_brain_connections")
            .select("connected_brain_id")
            .filter("composite_brain_id", "eq", str(composite_brain_id))
            .execute()
        )

        return [item["connected_brain_id"] for item in response.data]

    def disconnect_brain(
        self, composite_brain_id: UUID, connected_brain_id: UUID
    ) -> None:
        self.db.table("composite_brain_connections").delete().match(
            {
                "composite_brain_id": composite_brain_id,
                "connected_brain_id": connected_brain_id,
            }
        ).execute()

    def is_connected_brain(self, brain_id: UUID) -> bool:
        response = (
            self.db.from_("composite_brain_connections")
            .select("connected_brain_id")
            .filter("connected_brain_id", "eq", str(brain_id))
            .execute()
        )

        return len(response.data) > 0
