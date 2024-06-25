import React, { useState } from "react";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Knowledge } from "@/lib/types/Knowledge";

import KnowledgeItem from "./KnowledgeItem/KnowledgeItem";
import { useKnowledgeItem } from "./KnowledgeItem/hooks/useKnowledgeItem";
import styles from "./KnowledgeTable.module.scss";

interface KnowledgeTableProps {
  knowledgeList: Knowledge[];
}

const KnowledgeTable = React.forwardRef<HTMLDivElement, KnowledgeTableProps>(
  ({ knowledgeList }, ref) => {
    // Change selectedKnowledge to store Knowledge objects instead of string IDs
    const [selectedKnowledge, setSelectedKnowledge] = useState<Knowledge[]>([]);
    const [lastSelectedIndex, setLastSelectedIndex] = useState<number | null>(
      null
    );
    const { onDeleteKnowledge } = useKnowledgeItem();

    const handleSelect = (
      knowledge: Knowledge,
      index: number,
      event: React.MouseEvent
    ) => {
      if (event.shiftKey && lastSelectedIndex !== null) {
        const start = Math.min(lastSelectedIndex, index);
        const end = Math.max(lastSelectedIndex, index);
        const range = knowledgeList.slice(start, end + 1);

        setSelectedKnowledge((prevSelected) => {
          const newSelected = [...prevSelected];
          range.forEach((item) => {
            if (
              !newSelected.some((selectedItem) => selectedItem.id === item.id)
            ) {
              newSelected.push(item);
            }
          });

          return newSelected;
        });
      } else {
        const isSelected = selectedKnowledge.some(
          (item) => item.id === knowledge.id
        );
        setSelectedKnowledge((prevSelected) =>
          isSelected
            ? prevSelected.filter(
                (selectedItem) => selectedItem.id !== knowledge.id
              )
            : [...prevSelected, knowledge]
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
          <QuivrButton
            label="Clear all"
            iconName="delete"
            color="dangerous"
            onClick={() => {
              selectedKnowledge.forEach((knowledge) => {
                void onDeleteKnowledge(knowledge);
              });
              setSelectedKnowledge([]);
            }}
          />
        </div>
        <div>
          <div className={styles.first_line}>
            <span className={styles.name}>Name</span>
            <span className={styles.actions}>Actions</span>
          </div>
          {knowledgeList.map((knowledge, index) => (
            <div
              key={knowledge.id}
              onClick={(event) => handleSelect(knowledge, index, event)}
            >
              <KnowledgeItem
                knowledge={knowledge}
                selected={selectedKnowledge.some(
                  (item) => item.id === knowledge.id
                )}
                setSelected={(selected, event) =>
                  handleSelect(knowledge, index, event)
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
