import React, { useState } from "react";
import { FaCheckCircle, FaCopy } from "react-icons/fa";
import ReactMarkdown from "react-markdown";

import { cn } from "@/lib/utils";

import { QuestionBrain } from "./components/QuestionBrain";
import { QuestionPrompt } from "./components/QuestionPrompt";

type MessageRowProps = {
  speaker: string;
  text: string;
  brainName?: string | null;
  promptName?: string | null;
};

export const MessageRow = React.forwardRef(
  (
    { speaker, text, brainName, promptName }: MessageRowProps,
    ref: React.Ref<HTMLDivElement>
  ) => {
    const isUserSpeaker = speaker === "user";
    const [isCopied, setIsCopied] = useState(false);

    const handleCopy = () => {
      navigator.clipboard.writeText(text).then(
        () => setIsCopied(true),
        (err) => console.error("Failed to copy!", err)
      );
      setTimeout(() => setIsCopied(false), 2000); // Reset after 2 seconds
    };

    const containerClasses = cn(
      "py-3 px-5 w-fit",
      isUserSpeaker
        ? "bg-msg-gray bg-opacity-60 items-start"
        : "bg-msg-purple bg-opacity-60 items-end",
      "dark:bg-gray-800 rounded-3xl flex flex-col overflow-hidden scroll-pb-32"
    );

    const containerWrapperClasses = cn(
      "flex flex-col",
      isUserSpeaker ? "items-end" : "items-start"
    );

    const markdownClasses = cn("prose", "dark:prose-invert");

    return (
      <div className={containerWrapperClasses}>
        <div ref={ref} className={containerClasses}>
          <div className="w-full gap-1 flex justify-between">
            <div className="flex">
              <QuestionBrain brainName={brainName} />
              <QuestionPrompt promptName={promptName} />
            </div>
            {!isUserSpeaker && (
              <button
                className="text-gray-500 hover:text-gray-700 transition"
                onClick={handleCopy}
                title={isCopied ? "Copied!" : "Copy to clipboard"}
              >
                {isCopied ? <FaCheckCircle /> : <FaCopy />}
              </button>
            )}
          </div>
          <div data-testid="chat-message-text">
            <ReactMarkdown className={markdownClasses}>{text}</ReactMarkdown>
          </div>
        </div>
      </div>
    );
  }
);

MessageRow.displayName = "MessageRow";
