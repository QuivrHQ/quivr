import React from "react";

import { CopyButton } from "./components/CopyButton";
import { MessageContent } from "./components/MessageContent";
import { QuestionBrain } from "./components/QuestionBrain";
import { QuestionPrompt } from "./components/QuestionPrompt";
import { SourcesButton } from './components/SourcesButton'; // Import the new component
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

    let messageContent = text ?? "";
    let sourcesContent = "";

    const sourcesIndex = messageContent.lastIndexOf("**Sources:**");
    const hasSources = sourcesIndex !== -1;
    
    if (hasSources) {
      sourcesContent = messageContent.substring(sourcesIndex + "**Sources:**".length).trim();
      messageContent = messageContent.substring(0, sourcesIndex).trim();
    }

    return (
      <div className={containerWrapperClasses}>
        <div ref={ref} className={containerClasses}>
          <div className="flex justify-between items-start w-full">
            {/* Left section for the question and prompt */}
            <div className="flex">
              <QuestionBrain brainName={brainName} />
              <QuestionPrompt promptName={promptName} />
            </div>
            {/* Right section for buttons */}
            <div className="flex items-center gap-2">
              {!isUserSpeaker && (
                <>
                  {hasSources && <SourcesButton sources={sourcesContent} />}
                  <CopyButton handleCopy={handleCopy} isCopied={isCopied} />
                </>
              )}
            </div>
          </div>
          {children ?? (
            <MessageContent
              text={messageContent}
              markdownClasses={markdownClasses}
            />
          )}
        </div>
      </div>
    );
  }
);
    
MessageRow.displayName = "MessageRow";
