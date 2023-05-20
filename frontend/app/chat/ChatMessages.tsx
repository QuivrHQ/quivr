"use client";
import { cn } from "@/lib/utils";
import { FC, useEffect, useRef } from "react";

interface ChatMessagesProps {
  history: Array<[string, string]>;
}

const ChatMessages: FC<ChatMessagesProps> = ({ history }) => {
  const scrollableRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    scrollableRef.current?.scrollTo(0, scrollableRef.current.scrollHeight);
  }, [history]);

  return (
    <div
      ref={scrollableRef}
      className="mt-5 max-w-lg max-h-[50vh] overflow-y-auto flex flex-col gap-5 py-5 scrollbar"
    >
      {history.map(([speaker, text], idx) => {
        if (idx % 2 === 0)
          return <ChatMessage key={idx} speaker={speaker} text={text} />;
        else {
          return <ChatMessage key={idx} speaker={speaker} text={text} left />;
        }
      })}
    </div>
  );
};

const ChatMessage = ({
  speaker,
  text,
  left = false,
}: {
  speaker: string;
  text: string;
  left?: boolean;
}) => {
  return (
    <div
      className={cn(
        "py-3 px-3 rounded-lg border border-black/10 dark:border-white/25 w-fit flex flex-col min-w-[128px]",
        left ? "mr-20" : "self-end ml-20"
      )}
    >
      <span className={cn("capitalize text-xs")}>{speaker}</span>
      <p>{text}</p>
    </div>
  );
};

export default ChatMessages;
