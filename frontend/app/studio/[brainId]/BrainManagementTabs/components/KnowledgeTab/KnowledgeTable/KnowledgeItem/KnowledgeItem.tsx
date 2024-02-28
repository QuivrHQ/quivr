"use client";

import { useRef, useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { OptionsModal } from "@/lib/components/ui/OptionsModal/OptionsModal";
import { getFileIcon } from "@/lib/helpers/getFileIcon";
import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";
import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";
import { Option } from "@/lib/types/Options";

import { useKnowledgeItem } from "./hooks/useKnowledgeItem";
// eslint-disable-next-line import/order
import styles from "./KnowledgeItem.module.scss";

const KnowledgeItem = ({
  knowledge,
}: {
  knowledge: Knowledge;
}): JSX.Element => {
  const [optionsOpened, setOptionsOpened] = useState<boolean>(false);
  const iconRef = useRef<HTMLDivElement | null>(null);
  const optionsRef = useRef<HTMLDivElement | null>(null);
  const { onDeleteKnowledge } = useKnowledgeItem();
  const { brain } = useUrlBrain();

  const options: Option[] = [
    {
      label: "Delete",
      onClick: (knowledgeToRemove: Knowledge) =>
        void onDeleteKnowledge(knowledgeToRemove),
      iconName: "delete",
      iconColor: "dangerous",
      disabled: brain?.role !== "Owner",
    },
  ];

  return (
    <div className={styles.knowledge_item_wrapper}>
      <div className={styles.left}>
        {isUploadedKnowledge(knowledge) ? (
          getFileIcon(knowledge.fileName)
        ) : (
          <Icon name="link" size="normal" color="black" />
        )}
        {isUploadedKnowledge(knowledge) ? (
          <span>{knowledge.fileName}</span>
        ) : (
          <a href={knowledge.url} target="_blank" rel="noopener noreferrer">
            {knowledge.url}
          </a>
        )}
      </div>
      <div
        ref={iconRef}
        onClick={(event: React.MouseEvent<HTMLElement>) => {
          event.nativeEvent.stopImmediatePropagation();
          setOptionsOpened(!optionsOpened);
        }}
      >
        <Icon name="options" size="normal" color="black" handleHover={true} />
      </div>
      <div ref={optionsRef} className={styles.options_modal}>
        {optionsOpened && <OptionsModal options={options} />}
      </div>
      {/* <DownloadUploadedKnowledge knowledge={knowledge} /> */}
      {/* <DeleteKnowledge knowledge={knowledge} /> */}
    </div>
  );
};

export default KnowledgeItem;
