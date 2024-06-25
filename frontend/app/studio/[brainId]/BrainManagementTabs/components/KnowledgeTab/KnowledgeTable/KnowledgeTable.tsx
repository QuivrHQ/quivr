import React, { useState } from "react";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { Knowledge } from "@/lib/types/Knowledge";

import KnowledgeItem from "./KnowledgeItem/KnowledgeItem";
import { useKnowledgeItem } from "./KnowledgeItem/hooks/useKnowledgeItem";
import styles from "./KnowledgeTable.module.scss";

interface KnowledgeTableProps {
  knowledgeList: Knowledge[];
}

const KnowledgeTable = React.forwardRef<HTMLDivElement, KnowledgeTableProps>(
  ({ knowledgeList }, ref) => {
    const [selectedKnowledge, setSelectedKnowledge] = useState<Knowledge[]>([]);
    const [lastSelectedIndex, setLastSelectedIndex] = useState<number | null>(
      null
    );
    const { onDeleteKnowledge } = useKnowledgeItem();
    const [allChecked, setAllChecked] = useState<boolean>(false);
    const [searchQuery, setSearchQuery] = useState<string>("");

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
        <span className={styles.title}>Uploaded Knowledge</span>
        <div className={styles.table_header}>
          <div className={styles.search}>
            <TextInput
              iconName="search"
              label="Search"
              inputValue={searchQuery}
              setInputValue={setSearchQuery}
            />
          </div>
          <QuivrButton
            label="Delete"
            iconName="delete"
            color="dangerous"
            disabled={selectedKnowledge.length === 0}
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
            <div className={styles.left}>
              <Checkbox
                checked={allChecked}
                setChecked={(checked) => {
                  setAllChecked(checked);
                  checked
                    ? setSelectedKnowledge(knowledgeList)
                    : setSelectedKnowledge([]);
                }}
              />
              <span className={styles.name}>Name</span>
            </div>
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
                setSelected={(_selected, event) =>
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
