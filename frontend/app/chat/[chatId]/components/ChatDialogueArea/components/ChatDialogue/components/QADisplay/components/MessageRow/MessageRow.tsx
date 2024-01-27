import React from "react";

import styles from "./MessageRow.module.scss";
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
  metadata?: {
    sources?: [string] | [];
  };
};

export const MessageRow = React.forwardRef(
  (
    { speaker, text, brainName, promptName, children }: MessageRowProps,
    ref: React.Ref<HTMLDivElement>
  ) => {
    const { handleCopy, isCopied, isUserSpeaker, markdownClasses } =
      useMessageRow({
        speaker,
        text,
      });

    const messageContent = text ?? "";

    return (
      <div
        ref={ref}
        className={`
      ${styles.message_row_container ?? ""} 
      ${isUserSpeaker ? styles.user ?? "" : styles.brain ?? ""}
      `}
      >
        {!isUserSpeaker && (
          <div className="flex justify-between items-start w-full">
            <div className="flex gap-1">
              <QuestionBrain brainName={brainName} />
              <QuestionPrompt promptName={promptName} />
            </div>
            <div className="flex items-center gap-2">
              <>
                <CopyButton handleCopy={handleCopy} isCopied={isCopied} />
              </>
            </div>
          </div>
        )}
        {children ?? (
          <MessageContent
            text={messageContent}
            markdownClasses={markdownClasses}
          />
        )}
      </div>
    );
  }
);

MessageRow.displayName = "MessageRow";
