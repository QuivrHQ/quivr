"use client";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";
import { FC, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

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
      className="mt-5 max-h-[50vh] overflow-y-auto flex flex-col gap-5 py-5 scrollbar scroll-smooth"
    >
      {history.length === 0 ? (
        <div className="text-center opacity-50">
          Start a conversation with your brain
        </div>
      ) : (
        <AnimatePresence initial={false}>
          {history.map(([speaker, text], idx) => {
            if (idx % 2 === 0)
              return <ChatMessage key={idx} speaker={speaker} text={text} />;
            else {
              return (
                <ChatMessage key={idx} speaker={speaker} text={text} left />
              );
            }
          })}
        </AnimatePresence>
      )}
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
    <motion.div
      initial={{ x: left ? -64 : 64, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: left ? 64 : -64, opacity: 0 }}
      className={cn(
        "py-3 px-3 rounded-lg prose border border-black/10 dark:border-white/25 w-fit flex flex-col min-w-[10vw] max-w-lg",
        left ? "mr-20" : "self-end ml-20"
      )}
    >
      <span className={cn("capitalize text-xs")}>{speaker}</span>
      <>
        <ReactMarkdown
          // remarkRehypeOptions={{}}
          className="prose"
        >
          {text}
        </ReactMarkdown>
      </>
    </motion.div>
  );
};

export default ChatMessages;
