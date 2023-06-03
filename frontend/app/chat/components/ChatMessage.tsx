import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { forwardRef, Ref } from "react";
import ReactMarkdown from "react-markdown";

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

ChatMessage.displayName = "ChatMessage";

export default ChatMessage;
