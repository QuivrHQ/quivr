import { useTranslation } from "react-i18next";

import { ChatItem } from "@/app/chat/[chatId]/components/ChatDialogueArea//components/ChatDialogue/components/ChatItem";
import {
  chatDialogueContainerClassName,
  chatItemContainerClassName,
} from "@/app/chat/[chatId]/components/ChatDialogueArea//components/ChatDialogue/styles";
import { getKeyFromChatItem } from "@/app/chat/[chatId]/components/ChatDialogueArea/components/ChatDialogue/utils/getKeyFromChatItem";
import { useChatContext } from "@/lib/context";

export const DisplayChatMessageArea = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  const { sharedChatItems } = useChatContext();

  return (
    <div className={chatDialogueContainerClassName}>
      {sharedChatItems.length === 0 ? (
        <div
          data-testid="empty-history-message"
          className="text-center opacity-50"
        >
          {t("ask", { ns: "chat" })}
        </div>
      ) : (
        <div>
          <div className={chatItemContainerClassName}>
            {sharedChatItems.map((chatItem) => (
              <ChatItem key={getKeyFromChatItem(chatItem)} content={chatItem} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
