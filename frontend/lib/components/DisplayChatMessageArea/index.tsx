"use client";

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ChatItem } from "@/app/chat/[chatId]/components/ChatDialogueArea//components/ChatDialogue/components/ChatItem";
import {
  chatDialogueContainerClassName,
  chatItemContainerClassName,
} from "@/app/chat/[chatId]/components/ChatDialogueArea//components/ChatDialogue/styles";
import { getKeyFromChatItem } from "@/app/chat/[chatId]/components/ChatDialogueArea/components/ChatDialogue/utils/getKeyFromChatItem";
import { ChatItemWithGroupedNotifications } from "@/app/chat/[chatId]/components/ChatDialogueArea/types";
import { getMergedChatMessagesWithDoneStatusNotificationsReduced } from "@/app/chat/[chatId]/components/ChatDialogueArea/utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";
import { useSharedChatItems } from "@/app/shared/components/hooks/useSharedChatItems";
import { useChatContext } from "@/lib/context";
export const DisplayChatMessageArea = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  useSharedChatItems();
  const { messages, notifications } = useChatContext();

  const [chatItems, setChatItems] = useState<
    ChatItemWithGroupedNotifications[]
  >([]);

  useEffect(() => {
    if (notifications.length > 0 || messages.length > 0) {
      const mergedChatItems =
        getMergedChatMessagesWithDoneStatusNotificationsReduced(
          messages,
          notifications
        );
      setChatItems(mergedChatItems);
    }
  }, [messages, notifications]);

  return (
    <div className={chatDialogueContainerClassName}>
      {chatItems.length === 0 ? (
        <div
          data-testid="empty-history-message"
          className="text-center opacity-50"
        >
          {t("ask", { ns: "chat" })}
        </div>
      ) : (
        <div>
          <div className={chatItemContainerClassName}>
            {chatItems.map((chatItem) => (
              <ChatItem key={getKeyFromChatItem(chatItem)} content={chatItem} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
