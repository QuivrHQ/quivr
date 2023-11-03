import { useTranslation } from "react-i18next";

import { ChatItem } from "@/app/chat/[chatId]/components/ChatDialogueArea//components/ChatDialogue/components/ChatItem";
import {
  chatDialogueContainerClassName,
  chatItemContainerClassName,
} from "@/app/chat/[chatId]/components/ChatDialogueArea//components/ChatDialogue/styles";
import { getKeyFromChatItem } from "@/app/chat/[chatId]/components/ChatDialogueArea/components/ChatDialogue/utils/getKeyFromChatItem";
import { ChatItemWithGroupedNotifications } from "@/app/chat/[chatId]/components/ChatDialogueArea/types";

type MessagesDialogueProps = {
  chatItems: ChatItemWithGroupedNotifications[];
};

export const DisplayChatMessageArea = ({
  chatItems,
}: MessagesDialogueProps): JSX.Element => {
  const { t } = useTranslation(["chat"]);

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
