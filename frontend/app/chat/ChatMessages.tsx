"use client";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";
import { FC, Ref, forwardRef, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

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
            if (idx % 2 === 0)
              return (
                <ChatMessage
                  ref={idx === history.length - 1 ? lastChatRef : null}
                  key={idx}
                  speaker={speaker}
                  text={text}
                />
              );
            else {
              return (
                <ChatMessage
                  ref={idx === history.length - 1 ? lastChatRef : null}
                  key={idx}
                  speaker={speaker}
                  text={text}
                  left
                />
              );
            }
          })}
        </AnimatePresence>
      )}
    </div>
  );
};

const ChatMessage = forwardRef(
  (
    {
      speaker,
      text,
      left = false,
    }: {
      speaker: string;
      text: string;
      left?: boolean;
    },
    ref
  ) => {
    return (
      <motion.div
        ref={ref as Ref<HTMLDivElement>}
        initial={{ y: -24, opacity: 0 }}
        animate={{
          y: 0,
          opacity: 1,
          transition: { duration: 0.2, ease: "easeOut" },
        }}
        exit={{ y: -24, opacity: 0 }}
        className={cn(
          "py-3 px-3 rounded-lg border border-black/10 dark:border-white/25 flex flex-col max-w-4xl overflow-hidden scroll-pt-32",
          left ? "self-start mr-20" : "self-end ml-20"
        )}
      >
        <span className={cn("capitalize text-xs")}>{speaker}</span>
        <>
          <ReactMarkdown
            // remarkRehypeOptions={{}}
            className="prose dark:prose-invert"
          >
            {text}
          </ReactMarkdown>
        </>
      </motion.div>
    );
  }
);

ChatMessage.displayName = 'ChatMessage';

export default ChatMessages;
