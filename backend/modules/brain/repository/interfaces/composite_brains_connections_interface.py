from abc import ABC, abstractmethod
from uuid import UUID

from modules.brain.entity.composite_brain_connection_entity import (
    CompositeBrainConnectionEntity,
)


class CompositeBrainsConnectionsInterface(ABC):
    @abstractmethod
    def connect_brain(
        self, composite_brain_id: UUID, connected_brain_id: UUID
    ) -> CompositeBrainConnectionEntity:
        """
        Connect a brain to a composite brain in the composite_brain_connections table
        """
        pass

    @abstractmethod
    def get_connected_brains(self, composite_brain_id: UUID) -> list[UUID]:
        """
        Get all brains connected to a composite brain
        """
        pass

    @abstractmethod
    def disconnect_brain(
        self, composite_brain_id: UUID, connected_brain_id: UUID
    ) -> None:
        """
        Disconnect a brain from a composite brain
        """
        pass

    @abstractmethod
    def is_connected_brain(self, brain_id: UUID) -> bool:
        """
        Check if a brain is connected to any composite brain
        """
        pass
