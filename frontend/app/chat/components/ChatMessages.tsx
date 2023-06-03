"use client";
import { AnimatePresence } from "framer-motion";
import { FC, useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";

interface ChatMessagesProps {
  history: Array<[string, string]>;
}

const ChatMessages: FC<ChatMessagesProps> = ({ history }) => {
  const lastChatRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    lastChatRef.current?.scrollIntoView({ behavior: "auto", block: "start" });
  }, [history]);

  return (
    <div className="overflow-hidden flex flex-col gap-5 scrollbar scroll-smooth">
      {history.length === 0 ? (
        <div className="text-center opacity-50">
          Ask a question, or describe a task.
        </div>
      ) : (
        <AnimatePresence initial={false}>
          {history.map(([speaker, text], idx) => {
            return (
              <ChatMessage
                ref={idx === history.length - 1 ? lastChatRef : null}
                key={idx}
                speaker={speaker}
                text={text}
                left={idx % 2 !== 0}
              />
            );
          })}
        </AnimatePresence>
      )}
    </div>
  );
};
export default ChatMessages;
