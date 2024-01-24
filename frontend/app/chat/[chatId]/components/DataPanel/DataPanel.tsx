"use client";

import { useEffect, useState } from "react";

import { useChatContext } from "@/lib/context";
import { CloseBrain } from "@/lib/types/MessageMetadata";

import styles from "./DataPanel.module.scss";
import RelatedBrains from "./components/RelatedBrains/RelatedBrains";

const DataPanel = (): JSX.Element => {
  const { messages } = useChatContext();
  const [lastMessageRelatedBrain, setLastMessageRelatedBrain] = useState<
    CloseBrain[]
  >([]);

  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage?.metadata?.close_brains) {
        setLastMessageRelatedBrain(lastMessage.metadata.close_brains);
      }
    }
  }, [lastMessageRelatedBrain, messages]);

  return (
    <div className={styles.data_panel_wrapper}>
      <RelatedBrains closeBrains={lastMessageRelatedBrain} />
    </div>
  );
};

export default DataPanel;
