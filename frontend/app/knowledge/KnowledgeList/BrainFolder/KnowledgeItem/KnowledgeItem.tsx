"use client";

import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";

import styles from "./KnowledgeItem.module.scss";

type KnowledgeItemProps = {
  knowledge: Knowledge;
};

const KnowledgeItem = ({ knowledge }: KnowledgeItemProps): JSX.Element => {
  return (
    <div className={styles.knowledge_item_wrapper}>
      {isUploadedKnowledge(knowledge) ? (
        <span className={styles.file_name}>{knowledge.fileName}</span>
      ) : (
        <a href={knowledge.url} target="_blank" rel="noopener noreferrer">
          {knowledge.url}
        </a>
      )}
    </div>
  );
};

export default KnowledgeItem;
