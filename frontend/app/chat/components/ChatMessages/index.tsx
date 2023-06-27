import React from "react";

import Card from "@/lib/components/ui/Card";

import { ChatMessage } from "./components/ChatMessage";
import { useChatMessages } from "./hooks/useChatMessages";
import { useChatContext } from "../../[chatId]/context/ChatContext";

export const ChatMessages = (): JSX.Element => {
  const { chatListRef } = useChatMessages();
  const { history } = useChatContext();

  return (
    <Card
      className="p-5 max-w-3xl w-full flex flex-col mb-8 overflow-y-auto"
      ref={chatListRef}
    >
      <div className="flex-1">
        {history.length === 0 ? (
          <div className="text-center opacity-50">
            Ask a question, or describe a task.
          </div>
        ) : (
          history.map(({ assistant, message_id, user_message }) => (
            <React.Fragment key={message_id}>
              <ChatMessage
                key={`user-${message_id}`}
                speaker={"user"}
                text={user_message}
              />
              <ChatMessage
                key={`assistant-${message_id}`}
                speaker={"assistant"}
                text={assistant}
              />
            </React.Fragment>
          ))
        )}
      </div>
    </Card>
  );
};
