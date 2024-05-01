import React, { useEffect, useState } from "react";

import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { CopyButton } from "@/lib/components/ui/CopyButton";
import Icon from "@/lib/components/ui/Icon/Icon";
import { Source } from "@/lib/types/MessageMetadata";

import styles from "./MessageRow.module.scss";
import { Citation } from "./components/Citation/Citation";
import { MessageContent } from "./components/MessageContent/MessageContent";
import { QuestionBrain } from "./components/QuestionBrain/QuestionBrain";
import { QuestionPrompt } from "./components/QuestionPrompt/QuestionPrompt";
import { SourceCitations } from "./components/Source/Source";
import { useMessageRow } from "./hooks/useMessageRow";
import { SourceFile } from "./types/types";

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
  messageId?: string;
  thumbs?: boolean;
  lastMessage?: boolean;
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
      messageId,
      thumbs: initialThumbs,
      lastMessage,
      metadata,
    }: MessageRowProps,
    ref: React.Ref<HTMLDivElement>
  ) => {
    const { handleCopy, isUserSpeaker } = useMessageRow({
      speaker,
      text,
    });
    const { updateChatMessage } = useChatApi();
    const { chatId } = useChat();
    const [thumbs, setThumbs] = useState<boolean | undefined | null>(
      initialThumbs
    );
    const [sourceFiles, setSourceFiles] = useState<SourceFile[]>([]);
    const [selectedSourceFile, setSelectedSourceFile] =
      useState<SourceFile | null>(null);

    const handleSourceFileClick = (sourceFile: SourceFile) => {
      setSelectedSourceFile((prev) =>
        prev && prev.filename === sourceFile.filename ? null : sourceFile
      );
    };

    useEffect(() => {
      setThumbs(initialThumbs);
      setSourceFiles(
        metadata?.sources?.reduce((acc, source) => {
          const existingSource = acc.find((s) => s.filename === source.name);
          if (existingSource) {
            existingSource.citations.push(source.citation);
          } else {
            acc.push({
              filename: source.name,
              file_url: source.source_url,
              citations: [source.citation],
              selected: false,
            });
          }

          return acc;
        }, [] as SourceFile[]) ?? []
      );
    }, [initialThumbs, metadata]);

    const messageContent = text ?? "";

    const thumbsUp = async () => {
      if (chatId && messageId) {
        await updateChatMessage(chatId, messageId, {
          thumbs: thumbs ? null : true,
        });
        setThumbs(thumbs ? null : true);
      }
    };

    const thumbsDown = async () => {
      if (chatId && messageId) {
        await updateChatMessage(chatId, messageId, {
          thumbs: thumbs === false ? null : false,
        });
        setThumbs(thumbs === false ? null : false);
      }
    };

    const renderMessageHeader = () => {
      if (!isUserSpeaker) {
        return (
          <div className={styles.message_header}>
            <QuestionBrain brainName={brainName} brainId={brainId} />
            <QuestionPrompt promptName={promptName} />
          </div>
        );
      } else {
        return (
          <div className={styles.message_header}>
            <Icon name="user" color="dark-grey" size="normal" />
            <span className={styles.me}>Me</span>
          </div>
        );
      }
    };

    const renderMetadata = () => {
      if (!isUserSpeaker && messageContent !== "🧠") {
        return (
          <div
            className={`${styles.metadata_wrapper} ${
              lastMessage ? styles.sticky : ""
            }`}
          >
            <div className={styles.sources_and_citations_wrapper}>
              <div className={styles.sources}>
                {sourceFiles.map((sourceFile, i) => (
                  <div
                    key={i}
                    onClick={() => handleSourceFileClick(sourceFile)}
                  >
                    <SourceCitations
                      sourceFile={sourceFile}
                      isSelected={
                        !!selectedSourceFile &&
                        selectedSourceFile.filename === sourceFile.filename
                      }
                    />
                  </div>
                ))}
              </div>

              {selectedSourceFile && (
                <div className={styles.citations}>
                  <div className={styles.file_name_wrapper}>
                    <span className={styles.box_title}>Source:</span>
                    <a
                      href={selectedSourceFile.file_url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <span className={styles.source}>
                        {selectedSourceFile.filename}
                      </span>
                    </a>
                  </div>
                  {selectedSourceFile.citations.map((citation, i) => (
                    <div key={i}>
                      <Citation citation={citation} />
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className={styles.icons_wrapper}>
              <CopyButton handleCopy={handleCopy} size="normal" />
              <Icon
                name="thumbsUp"
                handleHover={true}
                color={thumbs ? "primary" : "black"}
                size="normal"
                onClick={async () => {
                  await thumbsUp();
                }}
              />
              <Icon
                name="thumbsDown"
                handleHover={true}
                color={thumbs === false ? "primary" : "black"}
                size="normal"
                onClick={async () => {
                  await thumbsDown();
                }}
              />
            </div>
          </div>
        );
      }
    };

    return (
      <div
        className={`
      ${styles.message_row_container} 
      ${isUserSpeaker ? styles.user : styles.brain}
      `}
      >
        {renderMessageHeader()}
        <div ref={ref} className={styles.message_row_content}>
          {children ?? (
            <>
              <MessageContent text={messageContent} isUser={isUserSpeaker} />
            </>
          )}
        </div>
        {renderMetadata()}
      </div>
    );
  }
);

MessageRow.displayName = "MessageRow";
