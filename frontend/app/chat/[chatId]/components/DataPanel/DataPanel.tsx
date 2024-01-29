"use client";

import { useEffect, useState } from "react";

import { useChatContext } from "@/lib/context";
import { MessageMetadata, Source } from "@/lib/types/MessageMetadata";

import styles from "./DataPanel.module.scss";
import RelatedBrains from "./components/RelatedBrains/RelatedBrains";
import Sources from "./components/Sources/Sources";

const DataPanel = (): JSX.Element => {
  const { messages } = useChatContext();
  const [lastMessageMetadata, setLastMessageMetadata] =
    useState<MessageMetadata>();

  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      const newSources: Source[] = lastMessage.metadata?.sources ?? [];

      const updatedSources: Source[] = lastMessageMetadata?.sources
        ? [...lastMessageMetadata.sources]
        : [];

      newSources.forEach((source) => {
        const existingSource = updatedSources.find(
          (s) => s.source_url === source.source_url
        );
        if (existingSource) {
          existingSource.frequency += 1;
        } else {
          updatedSources.push(source);
        }
      });

      setLastMessageMetadata({
        closeBrains: lastMessage.metadata?.close_brains ?? [],
        sources: updatedSources,
      });
    }
  }, [messages]);

  return (
    <div className={styles.data_panel_wrapper}>
      <RelatedBrains closeBrains={lastMessageMetadata?.closeBrains} />
      <Sources sources={lastMessageMetadata?.sources} />
    </div>
  );
};

export default DataPanel;
