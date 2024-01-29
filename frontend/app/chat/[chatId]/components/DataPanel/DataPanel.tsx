"use client";

import { useEffect, useState } from "react";

import { useChatContext } from "@/lib/context";
import { MessageMetadata } from "@/lib/types/MessageMetadata";

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
      setLastMessageMetadata({
        closeBrains: lastMessage.metadata?.close_brains ?? [],
        sources: lastMessage.metadata?.sources ?? [],
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
