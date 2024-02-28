import { Knowledge } from "@/lib/types/Knowledge";

import KnowledgeItem from "./KnowledgeItem/KnowledgeItem";
import styles from "./KnowledgeTable.module.scss";

interface KnowledgeTableProps {
  knowledgeList: Knowledge[];
}

export const KnowledgeTable = ({
  knowledgeList,
}: KnowledgeTableProps): JSX.Element => {
  return (
    <div className={styles.knowledge_table_wrapper}>
      <span className={styles.title}>Uploaded Knowledge</span>
      <div>
        {knowledgeList.map((knowledge) => (
          <KnowledgeItem knowledge={knowledge} key={knowledge.id} />
        ))}
      </div>
    </div>
  );
};
