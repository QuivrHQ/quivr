"use client";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { forwardRef, Ref } from "react";
import ReactMarkdown from "react-markdown";

const ChatMessage = forwardRef(
  (
    {
      speaker,
      text,
    }: {
      speaker: string;
      text: string;
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
          "py-3 px-3 md:px-6 w-full dark:border-white/25 flex flex-col max-w-4xl overflow-hidden scroll-pt-32",
          speaker === "user"
            ? ""
            : "bg-gray-200 dark:bg-gray-800 bg-opacity-60 py-8"
        )}
        style={speaker === "user" ? { whiteSpace: "pre-line" } : {}} // Add this line to preserve line breaks
      >
        <span
          className={cn(
            "capitalize  text-xs bg-sky-200 rounded-xl p-1 px-2 mb-2 w-fit  dark:bg-sky-700"
          )}
        >
          {speaker}
        </span>
        <>
          <ReactMarkdown
            // remarkRehypeOptions={{}}
            className="prose dark:prose-invert ml-[6px]  mt-1"
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
