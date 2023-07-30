from dataclasses import asdict, dataclass


@dataclass
class Chat:
    chat_id: str
    user_id: str
    creation_time: str
    chat_name: str

    def __init__(self, chat_dict: dict):
        self.chat_id = chat_dict.get(
            "chat_id"
        )  # pyright: ignore reportPrivateUsage=none
        self.user_id = chat_dict.get(
            "user_id"
        )  # pyright: ignore reportPrivateUsage=none
        self.creation_time = chat_dict.get(
            "creation_time"
        )  # pyright: ignore reportPrivateUsage=none
        self.chat_name = chat_dict.get(
            "chat_name"
        )  # pyright: ignore reportPrivateUsage=none


@dataclass
class ChatHistory:
    chat_id: str
    message_id: str
    user_message: str
    assistant: str
    message_time: str

    def __init__(self, chat_dict: dict):
        self.chat_id = chat_dict.get(
            "chat_id"
        )  # pyright: ignore reportPrivateUsage=none
        self.message_id = chat_dict.get(
            "message_id"
        )  # pyright: ignore reportPrivateUsage=none
        self.user_message = chat_dict.get(
            "user_message"
        )  # pyright: ignore reportPrivateUsage=none
        self.assistant = chat_dict.get(
            "assistant"
        )  # pyright: ignore reportPrivateUsage=none
        self.message_time = chat_dict.get(
            "message_time"
        )  # pyright: ignore reportPrivateUsage=none

    def to_dict(self):
        return asdict(self)
