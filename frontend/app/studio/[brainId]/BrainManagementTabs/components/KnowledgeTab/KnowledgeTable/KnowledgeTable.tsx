import React, { useEffect, useState } from "react";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { useDevice } from "@/lib/hooks/useDevice";
import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";

import { useKnowledgeItem } from "./KnowledgeItem/hooks/useKnowledgeItem";
// eslint-disable-next-line import/order
import KnowledgeItem from "./KnowledgeItem/KnowledgeItem";
import styles from "./KnowledgeTable.module.scss";

interface KnowledgeTableProps {
  knowledgeList: Knowledge[];
}

const filterAndSortKnowledge = (
  knowledgeList: Knowledge[],
  searchQuery: string,
  sortConfig: { key: string; direction: string }
): Knowledge[] => {
  let filteredList = knowledgeList.filter((knowledge) =>
    isUploadedKnowledge(knowledge)
      ? knowledge.fileName.toLowerCase().includes(searchQuery.toLowerCase())
      : knowledge.url.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (sortConfig.key) {
    const compareStrings = (a: string | number, b: string | number) => {
      if (a < b) {
        return sortConfig.direction === "ascending" ? -1 : 1;
      }
      if (a > b) {
        return sortConfig.direction === "ascending" ? 1 : -1;
      }

      return 0;
    };

    const getComparableValue = (item: Knowledge) => {
      if (sortConfig.key === "name") {
        return isUploadedKnowledge(item) ? item.fileName : item.url;
      }
      if (sortConfig.key === "status") {
        return item.status;
      }

      return "";
    };

    filteredList = filteredList.sort((a, b) =>
      compareStrings(getComparableValue(a), getComparableValue(b))
    );
  }

  return filteredList;
};

const updateSelectedKnowledge = ({
  knowledge,
  index,
  event,
  lastSelectedIndex,
  filteredKnowledgeList,
  selectedKnowledge,
}: {
  knowledge: Knowledge;
  index: number;
  event: React.MouseEvent;
  lastSelectedIndex: number | null;
  filteredKnowledgeList: Knowledge[];
  selectedKnowledge: Knowledge[];
}): { selectedKnowledge: Knowledge[]; lastSelectedIndex: number | null } => {
  if (event.shiftKey && lastSelectedIndex !== null) {
    const start = Math.min(lastSelectedIndex, index);
    const end = Math.max(lastSelectedIndex, index);
    const range = filteredKnowledgeList.slice(start, end + 1);

    const newSelected = [...selectedKnowledge];
    range.forEach((item) => {
      if (!newSelected.some((selectedItem) => selectedItem.id === item.id)) {
        newSelected.push(item);
      }
    });

    return { selectedKnowledge: newSelected, lastSelectedIndex: index };
  } else {
    const isSelected = selectedKnowledge.some(
      (item) => item.id === knowledge.id
    );
    const newSelectedKnowledge = isSelected
      ? selectedKnowledge.filter(
          (selectedItem) => selectedItem.id !== knowledge.id
        )
      : [...selectedKnowledge, knowledge];

    return {
      selectedKnowledge: newSelectedKnowledge,
      lastSelectedIndex: isSelected ? null : index,
    };
  }
};

const KnowledgeTable = React.forwardRef<HTMLDivElement, KnowledgeTableProps>(
  ({ knowledgeList }, ref) => {
    const [selectedKnowledge, setSelectedKnowledge] = useState<Knowledge[]>([]);
    const [lastSelectedIndex, setLastSelectedIndex] = useState<number | null>(
      null
    );
    const { onDeleteKnowledge } = useKnowledgeItem();
    const [allChecked, setAllChecked] = useState<boolean>(false);
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [filteredKnowledgeList, setFilteredKnowledgeList] =
      useState<Knowledge[]>(knowledgeList);
    const { isMobile } = useDevice();
    const [sortConfig, setSortConfig] = useState<{
      key: string;
      direction: string;
    }>({ key: "", direction: "" });

    useEffect(() => {
      setFilteredKnowledgeList(
        filterAndSortKnowledge(knowledgeList, searchQuery, sortConfig)
      );
    }, [searchQuery, knowledgeList, sortConfig]);

    const handleSelect = (
      knowledge: Knowledge,
      index: number,
      event: React.MouseEvent
    ) => {
      const newSelectedKnowledge = updateSelectedKnowledge({
        knowledge,
        index,
        event,
        lastSelectedIndex,
        filteredKnowledgeList,
        selectedKnowledge,
      });
      setSelectedKnowledge(newSelectedKnowledge.selectedKnowledge);
      setLastSelectedIndex(newSelectedKnowledge.lastSelectedIndex);
    };

    const handleDelete = () => {
      const toDelete = selectedKnowledge.filter((knowledge) =>
        filteredKnowledgeList.some((item) => item.id === knowledge.id)
      );
      toDelete.forEach((knowledge) => {
        void onDeleteKnowledge(knowledge);
      });
      setSelectedKnowledge([]);
    };

    const handleSort = (key: string) => {
      setSortConfig((prevSortConfig) => {
        let direction = "ascending";
        if (
          prevSortConfig.key === key &&
          prevSortConfig.direction === "ascending"
        ) {
          direction = "descending";
        }

        return { key, direction };
      });
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
              small={true}
            />
          </div>
          <QuivrButton
            label="Delete"
            iconName="delete"
            color="dangerous"
            disabled={selectedKnowledge.length === 0}
            onClick={handleDelete}
          />
        </div>
        <div>
          <div
            className={`${styles.first_line} ${
              filteredKnowledgeList.length === 0 ? styles.empty : ""
            }`}
          >
            <div className={styles.left}>
              <Checkbox
                checked={allChecked}
                setChecked={(checked) => {
                  setAllChecked(checked);
                  setSelectedKnowledge(checked ? filteredKnowledgeList : []);
                }}
              />
              <div className={styles.name} onClick={() => handleSort("name")}>
                Name
                <div className={styles.icon}>
                  <Icon name="sort" size="small" color="black" />
                </div>
              </div>
            </div>
            <div className={styles.right}>
              {!isMobile && (
                <div
                  className={styles.status}
                  onClick={() => handleSort("status")}
                >
                  Status
                  <div className={styles.icon}>
                    <Icon name="sort" size="small" color="black" />
                  </div>
                </div>
              )}
              <span className={styles.actions}>Actions</span>
            </div>
          </div>
          {filteredKnowledgeList.map((knowledge, index) => (
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
                lastChild={index === filteredKnowledgeList.length - 1}
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
