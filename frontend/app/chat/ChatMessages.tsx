"use client";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";
import { FC, Ref, forwardRef, useEffect, useRef } from "react";
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
      className="overflow-y-auto flex flex-col gap-5 py-5 scrollbar scroll-smooth"
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
        initial={{ x: left ? -64 : 64, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: left ? 64 : -64, opacity: 0 }}
        className={cn(
          "py-3 px-3 rounded-lg border border-black/10 dark:border-white/25 flex flex-col max-w-4xl",
          left ? "mr-20" : "self-end ml-20"
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

export default ChatMessages;
