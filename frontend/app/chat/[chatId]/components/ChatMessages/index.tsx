import React from "react";
import { useTranslation } from "react-i18next";

import { useChatContext } from "@/lib/context";

import { ChatMessage } from "./components/ChatMessage/components/ChatMessage";

export const ChatMessages = (): JSX.Element => {
  const { history } = useChatContext();
  const { t } = useTranslation(["chat"]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        flex: 1, // Allow the component to grow within its flex container
        overflowY: "auto", // Enable vertical scrolling when content overflows
      }}
    >
      {history.length === 0 ? (
        <div
          data-testid="empty-history-message"
          className="text-center opacity-50"
        >
          {t("ask", { ns: "chat" })}
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {history.map(
            ({
              assistant,
              message_id,
              user_message,
              brain_name,
              prompt_title,
            }) => (
              <React.Fragment key={message_id}>
                <ChatMessage
                  key={`user-${message_id}`}
                  speaker={"user"}
                  text={user_message}
                  promptName={prompt_title}
                  brainName={brain_name}
                />
                <ChatMessage
                  key={`assistant-${message_id}`}
                  speaker={"assistant"}
                  text={assistant}
                  brainName={brain_name}
                  promptName={prompt_title}
                />
              </React.Fragment>
            )
          )}
        </div>
      )}
    </div>
  );
};
