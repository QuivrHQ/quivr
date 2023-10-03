import React from "react";

import { CopyButton } from "./components/CopyButton";
import { MessageContent } from "./components/MessageContent";
import { QuestionBrain } from "./components/QuestionBrain";
import { QuestionPrompt } from "./components/QuestionPrompt";
import { useMessageRow } from "./hooks/useMessageRow";

type MessageRowProps = {
  speaker: "user" | "assistant";
  text?: string;
  brainName?: string | null;
  promptName?: string | null;
  children?: React.ReactNode;
};

export const MessageRow = React.forwardRef(
  (
    { speaker, text, brainName, promptName, children }: MessageRowProps,
    ref: React.Ref<HTMLDivElement>
  ) => {
    const {
      containerClasses,
      containerWrapperClasses,
      handleCopy,
      isCopied,
      isUserSpeaker,
      markdownClasses,
    } = useMessageRow({
      speaker,
      text,
    });

    return (
      <div className={containerWrapperClasses}>
        <div ref={ref} className={containerClasses}>
          <div className="w-full gap-1 flex justify-between">
            <div className="flex">
              <QuestionBrain brainName={brainName} />
              <QuestionPrompt promptName={promptName} />
            </div>
            {!isUserSpeaker && text !== undefined && (
              <CopyButton handleCopy={handleCopy} isCopied={isCopied} />
            )}
          </div>
          {children ?? (
            <MessageContent
              text={text ?? ""}
              markdownClasses={markdownClasses}
            />
          )}
        </div>
      </div>
    );
  }
);

MessageRow.displayName = "MessageRow";
