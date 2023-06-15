/* eslint-disable */
"use client";
import { useEffect, useRef } from "react";

import Card from "@/lib/components/ui/Card";
import useChatsContext from "@/lib/context/ChatsProvider/hooks/useChatsContext";
import { ChatMessage } from "./ChatMessage";

export const ChatMessages = (): JSX.Element => {
  const lastChatRef = useRef<HTMLDivElement | null>(null);

  const { chat } = useChatsContext();

  useEffect(() => {
    if (!chat || !lastChatRef.current) {
      return;
    }

    // if (chat.history.length > 2) {
    lastChatRef.current.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
    // }
  }, [chat, lastChatRef]);

  if (!chat) {
    return <></>;
  }

  return (
    <Card className="p-5 max-w-3xl w-full flex flex-col h-full mb-8">
      <div className="flex-1">
        {chat.history.length === 0 ? (
          <div className="text-center opacity-50">
            Ask a question, or describe a task.
          </div>
        ) : (
          chat.history.map(([speaker, text], idx) => {
            return (
              <ChatMessage
                ref={idx === chat.history.length - 1 ? lastChatRef : null}
                key={idx}
                speaker={speaker}
                text={text}
              />
            );
          })
        )}
      </div>
    </Card>
  );
};
export default ChatMessages;
