"use client";
import Card from "@/app/components/ui/Card";
import { AnimatePresence } from "framer-motion";
import { useEffect, useRef } from "react";
import { Chat } from "../../types";
import ChatMessage from "./ChatMessage";

interface ChatMessagesProps {
  chat: Chat;
}

export const ChatMessages = ({ chat }: ChatMessagesProps): JSX.Element => {
  const lastChatRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (chat.history.length > 2) {
      lastChatRef.current?.scrollIntoView({ behavior: "auto", block: "start" });
    }
  }, [chat]);

  return (
    <Card className="p-5 max-w-3xl w-full flex flex-col h-full mb-8">
      <div className="flex-1">
        {chat.history.length === 0 ? (
          <div className="text-center opacity-50">
            Ask a question, or describe a task.
          </div>
        ) : (
          <AnimatePresence initial={false}>
            {chat.history.map(([speaker, text], idx) => {
              return (
                <ChatMessage
                  ref={idx === chat.history.length - 1 ? lastChatRef : null}
                  key={idx}
                  speaker={speaker}
                  text={text}
                />
              );
            })}
          </AnimatePresence>
        )}
      </div>
    </Card>
  );
};
export default ChatMessages;
