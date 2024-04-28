import React from "react";

import { Knowledge } from "@/lib/types/Knowledge";

import KnowledgeItem from "./KnowledgeItem/KnowledgeItem";
import styles from "./KnowledgeTable.module.scss";

interface KnowledgeTableProps {
  knowledgeList: Knowledge[];
}

const KnowledgeTable = React.forwardRef<HTMLDivElement, KnowledgeTableProps>(
  ({ knowledgeList }, ref) => {
    return (
      <div ref={ref} className={styles.knowledge_table_wrapper}>
        <span className={styles.title}>Uploaded Knowledge</span>
        <div>
          {knowledgeList.map((knowledge) => (
            <KnowledgeItem knowledge={knowledge} key={knowledge.id} />
          ))}
        </div>
      </div>
    );
  }
);

KnowledgeTable.displayName = "KnowledgeTable";

export default KnowledgeTable;
