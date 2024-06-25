import React, { useState } from "react";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Knowledge } from "@/lib/types/Knowledge";

import KnowledgeItem from "./KnowledgeItem/KnowledgeItem";
import styles from "./KnowledgeTable.module.scss";

interface KnowledgeTableProps {
  knowledgeList: Knowledge[];
}

const KnowledgeTable = React.forwardRef<HTMLDivElement, KnowledgeTableProps>(
  ({ knowledgeList }, ref) => {
    const [selectedKnowledge, setSelectedKnowledge] = useState<string[]>([]);
    const [lastSelectedIndex, setLastSelectedIndex] = useState<number | null>(
      null
    );

    const handleSelect = (
      knowledgeId: string,
      index: number,
      event: React.MouseEvent
    ) => {
      if (event.shiftKey && lastSelectedIndex !== null) {
        const start = Math.min(lastSelectedIndex, index);
        const end = Math.max(lastSelectedIndex, index);
        const range = knowledgeList
          .slice(start, end + 1)
          .map((item) => item.id);

        setSelectedKnowledge((prevSelected) => {
          const newSelected = [...prevSelected];
          range.forEach((id) => {
            if (!newSelected.includes(id)) {
              newSelected.push(id);
            }
          });

          return newSelected;
        });
      } else {
        const isSelected = selectedKnowledge.includes(knowledgeId);
        setSelectedKnowledge((prevSelected) =>
          isSelected
            ? prevSelected.filter((selectedId) => selectedId !== knowledgeId)
            : [...prevSelected, knowledgeId]
        );
        setLastSelectedIndex(
          isSelected && lastSelectedIndex === index ? null : index
        );
      }
    };

    return (
      <div ref={ref} className={styles.knowledge_table_wrapper}>
        <div className={styles.table_header}>
          <span className={styles.title}>Uploaded Knowledge</span>
          <QuivrButton label="Clear all" iconName="delete" color="dangerous" />
        </div>
        <div>
          <div className={styles.first_line}>
            <span className={styles.name}>Name</span>
            <span className={styles.actions}>Actions</span>
          </div>
          {knowledgeList.map((knowledge, index) => (
            <div
              key={knowledge.id}
              onClick={(event) => handleSelect(knowledge.id, index, event)}
            >
              <KnowledgeItem
                knowledge={knowledge}
                selected={selectedKnowledge.includes(knowledge.id)}
                setSelected={(selected, event) =>
                  handleSelect(knowledge.id, index, event)
                }
                lastChild={index === knowledgeList.length - 1}
              />
            </div>
          ))}
        </div>
      </div>
    );
  }
);

KnowledgeTable.displayName = "KnowledgeTable";

export default KnowledgeTable;
