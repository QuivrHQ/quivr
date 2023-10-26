from routes.chat.interface import ChatInterface


class BrainlessChat(ChatInterface):
    def validate_authorization(self, user_id, brain_id):
        pass
