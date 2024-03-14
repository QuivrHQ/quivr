import React from "react";

import { CopyButton } from "@/lib/components/ui/CopyButton";
import Icon from "@/lib/components/ui/Icon/Icon";
import { useChatContext } from "@/lib/context";
import { useDevice } from "@/lib/hooks/useDevice";
import { Source } from "@/lib/types/MessageMetadata";

import styles from "./MessageRow.module.scss";
import { MessageContent } from "./components/MessageContent/MessageContent";
import { QuestionBrain } from "./components/QuestionBrain/QuestionBrain";
import { QuestionPrompt } from "./components/QuestionPrompt/QuestionPrompt";
import { useMessageRow } from "./hooks/useMessageRow";

type MessageRowProps = {
  speaker: "user" | "assistant";
  text?: string;
  brainName?: string | null;
  promptName?: string | null;
  children?: React.ReactNode;
  metadata?: {
    sources?: Source[];
  };
  brainId?: string;
  index?: number;
};

export const MessageRow = React.forwardRef(
  (
    {
      speaker,
      text,
      brainName,
      promptName,
      children,
      brainId,
      index,
    }: MessageRowProps,
    ref: React.Ref<HTMLDivElement>
  ) => {
    const { handleCopy, isUserSpeaker } = useMessageRow({
      speaker,
      text,
    });
    const { setSourcesMessageIndex, sourcesMessageIndex } = useChatContext();
    const { isMobile } = useDevice();

    const messageContent = text ?? "";

    return (
      <div
        className={`
      ${styles.message_row_container} 
      ${isUserSpeaker ? styles.user : styles.brain}
      `}
      >
        {!isUserSpeaker ? (
          <div className={styles.message_header}>
            <QuestionBrain brainName={brainName} brainId={brainId} />
            <QuestionPrompt promptName={promptName} />
          </div>
        ) : (
          <div className={styles.message_header}>
            <Icon name="user" color="dark-grey" size="normal" />
            <span className={styles.me}>Me</span>
          </div>
        )}
        {}
        <div ref={ref} className={styles.message_row_content}>
          {children ?? (
            <>
              <MessageContent text={messageContent} isUser={isUserSpeaker} />
              {!isUserSpeaker && messageContent !== "🧠" && (
                <div className={styles.icons_wrapper}>
                  <CopyButton handleCopy={handleCopy} size="normal" />
                  {!isMobile && (
                    <div className={styles.sources_icon_wrapper}>
                      <Icon
                        name="file"
                        handleHover={true}
                        color={
                          sourcesMessageIndex === index ? "primary" : "black"
                        }
                        size="normal"
                        onClick={() => {
                          setSourcesMessageIndex(
                            sourcesMessageIndex === index ? undefined : index
                          );
                        }}
                      />
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    );
  }
);

MessageRow.displayName = "MessageRow";
