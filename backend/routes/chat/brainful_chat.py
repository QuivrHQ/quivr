from routes.authorizations.brain_authorization import validate_brain_authorization
from routes.authorizations.types import RoleEnum
from routes.chat.interface import ChatInterface


class BrainfulChat(ChatInterface):
    def validate_authorization(self, user_id, brain_id):
        if brain_id:
            validate_brain_authorization(
                brain_id=brain_id,
                user_id=user_id,
                required_roles=[RoleEnum.Viewer, RoleEnum.Editor, RoleEnum.Owner],
            )
