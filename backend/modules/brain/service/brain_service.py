from uuid import UUID

from modules.brain.repository.brains import Brain
from modules.brain.repository.interfaces.brains_interface import BrainsInterface
from modules.brain.repository.interfaces.brains_users_interface import (
    BrainsUsersInterface,
)


class BrainService:
    brain_repository: BrainsInterface
    brain_user_repository: BrainsUsersInterface

    def __init__(self):
        self.brain_repository = Brain()

    def get_brain_by_id(self, brain_id: UUID):
        return self.brain_repository.get_brain_by_id(brain_id)
