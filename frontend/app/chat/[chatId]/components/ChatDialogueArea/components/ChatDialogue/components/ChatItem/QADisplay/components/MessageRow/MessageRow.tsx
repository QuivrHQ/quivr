import React, { useEffect, useState } from "react";

import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { CopyButton } from "@/lib/components/ui/CopyButton";
import Icon from "@/lib/components/ui/Icon/Icon";
import { ThoughtsButton } from "@/lib/components/ui/ThoughtsButton";
import { Source } from "@/lib/types/MessageMetadata";

import styles from "./MessageRow.module.scss";
import { Citation } from "./components/Citation/Citation";
import { MessageContent } from "./components/MessageContent/MessageContent";
import { QuestionBrain } from "./components/QuestionBrain/QuestionBrain";
import { SourceCitations } from "./components/Source/Source";
import { useMessageRow } from "./hooks/useMessageRow";
import { SourceFile } from "./types/types";

type MessageRowProps = {
  speaker: "user" | "assistant";
  text?: string;
  brainName?: string | null;
  children?: React.ReactNode;
  metadata?: {
    sources?: Source[];
    thoughts?: string;
    followup_questions?: string[];
  };
  brainId?: string;
  index?: number;
  messageId?: string;
  thumbs?: boolean;
  lastMessage?: boolean;
};

const MessageRow = React.forwardRef(
  (
    {
      speaker,
      text,
      brainName,
      children,
      brainId,
      messageId,
      thumbs: initialThumbs,
      metadata,
      lastMessage,
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
          </div>
        );
      }
    };

    const renderMetadata = () => {
      if (!isUserSpeaker && messageContent !== "🧠") {
        return (
          <div className={styles.metadata_wrapper}>
            <div
              className={`${styles.icons_wrapper} ${
                sourceFiles.length === 0 ? styles.with_border : ""
              }`}
            >
              {metadata?.thoughts && metadata.thoughts.trim() !== "" && (
                <ThoughtsButton text={metadata.thoughts} size="small" />
              )}
              <CopyButton handleCopy={handleCopy} size="small" />
              <Icon
                name="thumbsUp"
                handleHover={true}
                color={thumbs ? "primary" : "black"}
                size="small"
                onClick={async () => {
                  await thumbsUp();
                }}
              />
              <Icon
                name="thumbsDown"
                handleHover={true}
                color={thumbs === false ? "primary" : "black"}
                size="small"
                onClick={async () => {
                  await thumbsDown();
                }}
              />
            </div>

            {sourceFiles.length > 0 && (
              <div className={styles.sources_and_citations_wrapper}>
                <div className={styles.title_wrapper}>
                  <Icon name="sources" size="normal" color="black" />
                  <span className={styles.title}>Sources</span>
                </div>
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
            )}
          </div>
        );
      }
    };

    const renderRelatedQuestions = () => {
      if (!isUserSpeaker) {
        return (
          <div className={styles.related_questions_wrapper}>
            <div className={styles.title_wrapper}>
              <Icon name="search" color="black" size="normal" />
              <span className={styles.title}>Follow up questions</span>
            </div>
            <div className={styles.questions_wrapper}>
              {metadata?.followup_questions?.map((question, index) => (
                <div className={styles.question} key={index}>
                  <Icon name="followUp" size="small" color="grey" />
                  <span className={styles.text}>{question}</span>
                </div>
              ))}
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
      ${lastMessage ? styles.last : ""}
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
        {renderRelatedQuestions()}
      </div>
    );
  }
);

MessageRow.displayName = "MessageRow";

export default MessageRow;
