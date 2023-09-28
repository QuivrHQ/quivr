import { useTranslation } from "react-i18next";

import { ChatItem } from "./components";
import { useChatDialogue } from "./hooks/useChatDialogue";
import { getKeyFromChatItem } from "./utils/getKeyFromChatItem";
import { ChatItemWithGroupedNotifications } from "../../types";

type MessagesDialogueProps = {
  chatItems: ChatItemWithGroupedNotifications[];
};

export const ChatDialogue = ({
  chatItems,
}: MessagesDialogueProps): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  const { chatListRef } = useChatDialogue();

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        flex: 1,
        overflowY: "auto",
        marginBottom: 10,
      }}
      ref={chatListRef}
    >
      {chatItems.length === 0 ? (
        <div
          data-testid="empty-history-message"
          className="text-center opacity-50"
        >
          {t("ask", { ns: "chat" })}
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {chatItems.map((chatItem) => (
            <ChatItem key={getKeyFromChatItem(chatItem)} content={chatItem} />
          ))}
        </div>
      )}
    </div>
  );
};
