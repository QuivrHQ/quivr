from datetime import datetime
from enum import Enum
from typing import List, Union

from models.notifications import Notification
from repository.chat.get_chat_history import GetChatHistoryOutput


def parse_message_time(message_time_str):
    return datetime.strptime(message_time_str, "%Y-%m-%d %H:%M:%S")


# Define an enum for item_type
class ItemTypeEnum(Enum):
    MESSAGE = "MESSAGE"
    NOTIFICATION = "NOTIFICATION"


class ChatItem:
    def __init__(
        self,
        item_type: ItemTypeEnum,
        item_body: Union[GetChatHistoryOutput, Notification],
    ):
        self.type = item_type
        self.body = item_body


def merge_chat_history_and_notifications(
    chat_history: List[GetChatHistoryOutput], notifications: List[Notification]
) -> List[ChatItem]:
    chat_history_and_notifications = chat_history + notifications

    chat_history_and_notifications.sort(
        key=lambda x: parse_message_time(x.message_time)
        if isinstance(x, GetChatHistoryOutput)
        else parse_message_time(x.datetime)
    )

    transformed_data = []
    for item in chat_history_and_notifications:
        if isinstance(item, GetChatHistoryOutput):
            item_type = ItemTypeEnum.MESSAGE
            item_body = item
        else:
            item_type = ItemTypeEnum.NOTIFICATION
            item_body = item
        transformed_item = ChatItem(item_type, item_body)
        transformed_data.append(transformed_item)

    return transformed_data
