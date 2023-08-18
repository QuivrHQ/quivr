import { useFeature } from "@growthbook/growthbook-react";
import React from "react";
import ReactMarkdown from "react-markdown";

import { cn } from "@/lib/utils";

type ChatMessageProps = {
  speaker: string;
  text: string;
  brainName?: string;
  promptName?: string;
};

export const ChatMessage = React.forwardRef(
  (
    { speaker, text, brainName, promptName }: ChatMessageProps,
    ref: React.Ref<HTMLDivElement>
  ) => {
    const isNewUxOn = useFeature("new-ux").on;

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

    const markdownClasses = cn(
      "prose",
      "dark:prose-invert"
    );

    return (
      <div className={containerWrapperClasses}>
        {" "}
        <div ref={ref} className={containerClasses}>
          {isNewUxOn && (
            <span
              data-testid="brain-prompt-tags"
              className="text-gray-400 mb-1"
            >
              @{brainName ?? "-"} #{promptName ?? "-"}
            </span>
          )}
          <div data-testid="chat-message-text">
            <ReactMarkdown className={markdownClasses}>{text}</ReactMarkdown>
          </div>
        </div>
      </div>
    );
  }
);

ChatMessage.displayName = "ChatMessage";
