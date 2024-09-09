from typing import List

from quivr_api.logger import get_logger
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.chat.dto.chats import ChatItem, ChatItemType
from quivr_api.modules.chat.dto.outputs import GetChatHistoryOutput
from quivr_api.modules.notification.entity.notification import Notification
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.prompt.service.prompt_service import PromptService

logger = get_logger(__name__)

prompt_service = PromptService()
brain_service = BrainService()
notification_service = NotificationService()


def merge_chat_history_and_notifications(
    chat_history: List[GetChatHistoryOutput], notifications: List[Notification]
) -> List[ChatItem]:
    chat_history_and_notifications = chat_history + notifications

    chat_history_and_notifications.sort(
        key=lambda x: (
            x.message_time
            if isinstance(x, GetChatHistoryOutput) and x.message_time
            else x.datetime
        )
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
