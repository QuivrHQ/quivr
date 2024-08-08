import { UUID } from "crypto";
import React, { useEffect, useState } from "react";

import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { Integration } from "@/lib/api/sync/types";
import { CopyButton } from "@/lib/components/ui/CopyButton";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { Source } from "@/lib/types/MessageMetadata";

import styles from "./MessageRow.module.scss";
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
    metadata_model?: {
      display_name: string;
      image_url: string;
      brain_id: UUID;
    };
  };
  index?: number;
  messageId?: string;
  thumbs?: boolean;
  lastMessage?: boolean;
};

export const MessageRow = ({
  speaker,
  text,
  brainName,
  children,
  messageId,
  thumbs: initialThumbs,
  metadata,
  lastMessage,
}: MessageRowProps): JSX.Element => {
  const { handleCopy, isUserSpeaker } = useMessageRow({
    speaker,
    text,
  });
  const { updateChatMessage } = useChatApi();
  const { chatId } = useChat();
  const [thumbs, setThumbs] = useState<boolean | undefined | null>(
    initialThumbs
  );
  const [folded, setFolded] = useState<boolean>(false);
  const [sourceFiles, setSourceFiles] = useState<SourceFile[]>([]);
  const { submitQuestion } = useChatInput();

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
            integration: source.integration as Integration,
            integration_link: source.integration_link,
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
    if (!isUserSpeaker && !folded) {
      return (
        <div className={styles.message_header_wrapper}>
          <div className={styles.message_header}>
            <QuestionBrain
              brainName={brainName}
              imageUrl={metadata?.metadata_model?.image_url ?? ""}
            />
          </div>
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
                  <div key={i}>
                    <SourceCitations sourceFile={sourceFile} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }
  };

  const renderRelatedQuestions = () => {
    if (
      !isUserSpeaker &&
      !folded &&
      (metadata?.followup_questions?.length ?? 0) > 0
    ) {
      return (
        <div className={styles.related_questions_wrapper}>
          <div className={styles.title_wrapper}>
            <Icon name="search" color="black" size="normal" />
            <span className={styles.title}>Follow up questions</span>
          </div>
          <div className={styles.questions_wrapper}>
            {metadata?.followup_questions?.map((question, index) => (
              <div
                className={styles.question}
                key={index}
                onClick={() => submitQuestion(question)}
              >
                <Icon name="followUp" size="small" color="grey" />
                <span className={styles.text}>{question}</span>
              </div>
            ))}
          </div>
        </div>
      );
    }
  };

  const renderOtherSections = () => {
    return (
      <>
        {!folded && renderMetadata()}
        {!folded && renderRelatedQuestions()}
      </>
    );
  };

  return (
    <div
      className={`
      ${styles.message_row_container} 
      ${isUserSpeaker ? styles.user : styles.brain}
      ${messageContent.length > 100 && isUserSpeaker ? styles.smaller : ""}
      ${lastMessage ? styles.last : ""}
      `}
    >
      {!isUserSpeaker && messageContent !== "🧠" && (
        <div onClick={() => setFolded(!folded)}>
          <Icon
            name="chevronDown"
            color="black"
            handleHover={true}
            size="normal"
            classname={`${styles.icon_rotate} ${
              folded ? styles.icon_rotate_down : styles.icon_rotate_up
            }`}
          />
        </div>
      )}
      {renderMessageHeader()}
      <div className={styles.message_row_content}>
        {children ?? (
          <>
            <MessageContent
              text={messageContent}
              isUser={isUserSpeaker}
              hide={folded}
            />
          </>
        )}
      </div>
      {renderOtherSections()}
    </div>
  );
};
