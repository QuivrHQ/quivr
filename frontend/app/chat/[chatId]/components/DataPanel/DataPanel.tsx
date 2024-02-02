"use client";

import { useEffect, useState } from "react";

import { useChatContext } from "@/lib/context";
import { MessageMetadata, Source } from "@/lib/types/MessageMetadata";

import styles from "./DataPanel.module.scss";
import RelatedBrains from "./components/RelatedBrains/RelatedBrains";
import Sources from "./components/Sources/Sources";

import { ChatMessage } from "../../types";

const DataPanel = (): JSX.Element => {
  const { messages } = useChatContext();
  const [lastMessageMetadata, setLastMessageMetadata] =
    useState<MessageMetadata>();

  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage: ChatMessage = messages[messages.length - 1];
      const newSources: Source[] = (lastMessage.metadata?.sources ?? []).map(
        (source: Source) => ({
          ...source,
          frequency: 0,
        })
      );

      const updatedSources: Source[] = [];

      newSources.forEach((newSource) => {
        const existingSourceIndex = updatedSources.findIndex(
          (source) => source.name.trim() === newSource.name.trim()
        );
        if (existingSourceIndex !== -1) {
          updatedSources[existingSourceIndex] = {
            ...updatedSources[existingSourceIndex],
            frequency: updatedSources[existingSourceIndex].frequency + 1,
          };
        } else {
          updatedSources.push(newSource);
        }
      });

      updatedSources.sort((a, b) => b.frequency - a.frequency);

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
