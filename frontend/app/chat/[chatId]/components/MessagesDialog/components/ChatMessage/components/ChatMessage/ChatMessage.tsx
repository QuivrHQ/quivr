import React from "react";
import ReactMarkdown from "react-markdown";

import { cn } from "@/lib/utils";

import { QuestionBrain } from "./components/QuestionBrain";
import { QuestionPrompt } from "./components/QuestionPrompt";

type ChatMessageProps = {
  speaker: string;
  text: string;
  brainName?: string | null;
  promptName?: string | null;
};

export const ChatMessage = React.forwardRef(
  (
    { speaker, text, brainName, promptName }: ChatMessageProps,
    ref: React.Ref<HTMLDivElement>
  ) => {
    const isUserSpeaker = speaker === "user";
    const containerClasses = cn(
      "py-3 px-5 w-fit ",
      isUserSpeaker
        ? "bg-gray-100 bg-opacity-60 items-start "
        : "bg-purple-100 bg-opacity-60 items-end",
      "dark:bg-gray-800 rounded-3xl flex flex-col overflow-hidden scroll-pb-32"
    );

    const containerWrapperClasses = cn(
      "flex flex-col",

      isUserSpeaker ? "items-end" : "items-start"
    );

    const markdownClasses = cn("prose", "dark:prose-invert");

    return (
      <div className={containerWrapperClasses}>
        {" "}
        <div ref={ref} className={containerClasses}>
          <div className="w-full gap-1 flex">
            <QuestionBrain brainName={brainName} />
            <QuestionPrompt promptName={promptName} />
          </div>
          <div data-testid="chat-message-text">
            <ReactMarkdown className={markdownClasses}>{text}</ReactMarkdown>
          </div>
        </div>
      </div>
    );
  }
);

ChatMessage.displayName = "ChatMessage";
