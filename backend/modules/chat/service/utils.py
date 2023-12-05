from typing import List

from logger import get_logger
from modules.brain.service.brain_service import BrainService
from modules.chat.dto.chats import ChatItem, ChatItemType
from modules.chat.dto.outputs import GetChatHistoryOutput
from modules.notification.entity.notification import Notification
from modules.notification.service.notification_service import NotificationService
from modules.prompt.service.prompt_service import PromptService
from packages.utils import parse_message_time

logger = get_logger(__name__)

prompt_service = PromptService()
brain_service = BrainService()
notification_service = NotificationService()


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
            item_type = ChatItemType.MESSAGE
            body = item
        else:
            item_type = ChatItemType.NOTIFICATION
            body = item
        transformed_item = ChatItem(item_type=item_type, body=body)
        transformed_data.append(transformed_item)

    return transformed_data
