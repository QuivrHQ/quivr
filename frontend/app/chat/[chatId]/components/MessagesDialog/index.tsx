import { useTranslation } from "react-i18next";

import { useChatContext } from "@/lib/context";

import { ChatMessage } from "./components";
import { useMessagesDialog } from "./hooks/useMessagesDialog";
import { getMergedChatHistoryWithReducedNotifications } from "./utils/getMergedChatHistoryWithReducedNotifications";

export const MessagesDialog = (): JSX.Element => {
  const { messages, notifications } = useChatContext();
  const { t } = useTranslation(["chat"]);
  const { chatListRef } = useMessagesDialog();

  const chatItems = getMergedChatHistoryWithReducedNotifications(
    messages,
    notifications
  );
  console.log({ chatItems });

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        flex: 1,
        overflowY: "auto",
      }}
      ref={chatListRef}
    >
      {messages.length === 0 ? (
        <div
          data-testid="empty-history-message"
          className="text-center opacity-50"
        >
          {t("ask", { ns: "chat" })}
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {messages.map((message) => (
            <ChatMessage key={message.message_id} content={message} />
          ))}
        </div>
      )}
    </div>
  );
};
