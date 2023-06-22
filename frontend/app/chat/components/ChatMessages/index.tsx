/* eslint-disable */
"use client";
import { useCallback, useEffect, useRef } from "react";

import Card from "@/lib/components/ui/Card";
import { useChat } from "../../[chatId]/hooks/useChat";
import { ChatMessage } from "./ChatMessage";

export const ChatMessages = (): JSX.Element => {
  const lastChatRef = useRef<HTMLDivElement | null>(null);
  const { history } = useChat();

  const scrollToBottom = useCallback(() => {
    if (lastChatRef.current) {
      lastChatRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [history, scrollToBottom]);

  return (
    <Card className="p-5 max-w-3xl w-full flex flex-col h-full mb-8">
      <div className="flex-1">
        {history.length === 0 ? (
          <div className="text-center opacity-50">
            Ask a question, or describe a task.
          </div>
        ) : (
          history.map(({ assistant, message_id, user_message }, idx) => (
            <>
              <ChatMessage
                key={message_id}
                speaker={"user"}
                text={user_message}
              />
              <ChatMessage
                key={message_id}
                speaker={"assistant"}
                text={assistant}
              />
            </>
          ))
        )}
        <div ref={lastChatRef} />
      </div>
    </Card>
  );
};
export default ChatMessages;
