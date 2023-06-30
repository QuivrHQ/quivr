from dataclasses import asdict, dataclass


@dataclass
class Chat:
    chat_id: str
    user_id: str
    creation_time: str
    chat_name: str

    def __init__(self, chat_dict: dict):
        self.chat_id = chat_dict.get("chat_id")
        self.user_id = chat_dict.get("user_id")
        self.creation_time = chat_dict.get("creation_time")
        self.chat_name = chat_dict.get("chat_name")


@dataclass
class ChatHistory:
    chat_id: str
    message_id: str
    user_message: str
    assistant: str
    message_time: str

    def __init__(self, chat_dict: dict):
        self.chat_id = chat_dict.get("chat_id")
        self.message_id = chat_dict.get("message_id")
        self.user_message = chat_dict.get("user_message")
        self.assistant = chat_dict.get("assistant")
        self.message_time = chat_dict.get("message_time")

    def to_dict(self):
        return asdict(self)
