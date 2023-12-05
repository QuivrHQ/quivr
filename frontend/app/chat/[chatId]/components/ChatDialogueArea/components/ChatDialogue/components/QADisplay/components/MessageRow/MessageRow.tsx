import Image from "next/image";
import React from "react";
import { FaCircleUser } from "react-icons/fa6";

import { CopyButton } from "./components/CopyButton";
import { MessageContent } from "./components/MessageContent";
import { QuestionBrain } from "./components/QuestionBrain";
import { QuestionPrompt } from "./components/QuestionPrompt";
import { SourcesButton } from "./components/SourcesButton";
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
      sourcesContent = messageContent
        .substring(sourcesIndex + "**Sources:**".length)
        .trim();
      messageContent = messageContent.substring(0, sourcesIndex).trim();
    }

    return (
      <div className={containerWrapperClasses}>
        <div ref={ref} className={containerClasses}>
          <div className="flex justify-between items-center w-full">
            <div className="flex items-center flex-1">
              {!isUserSpeaker && (
                <Image
                  className={"h-6 w-6 rounded-full mr-4"}
                  src={"/answer-bot.png"}
                  alt="answer-bot"
                  width={100}
                  height={100}
                ></Image>
              )}
              {/* Left section for the question and prompt */}
              <div className="flex hidden">
                <QuestionBrain brainName={brainName} />
                <QuestionPrompt promptName={promptName} />
              </div>
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

            {isUserSpeaker && <FaCircleUser className="h-6 w-6 rounded-full" />}
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
