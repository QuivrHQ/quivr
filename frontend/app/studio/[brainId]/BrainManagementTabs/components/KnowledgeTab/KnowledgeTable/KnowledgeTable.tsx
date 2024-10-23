import React, { useEffect, useState } from "react";

import { KMSElement } from "@/lib/api/sync/types";
import KnowledgeManagementSystem from "@/lib/components/KnowledgeManagementSystem/KnowledgeManagementSystem";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { SwitchButton } from "@/lib/components/ui/SwitchButton/SwitchButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { updateSelectedItems } from "@/lib/helpers/table";
import { useDevice } from "@/lib/hooks/useDevice";

import KnowledgeItem from "./KnowledgeItem/KnowledgeItem";
import { useKnowledgeItem } from "./KnowledgeItem/hooks/useKnowledgeItem";
import styles from "./KnowledgeTable.module.scss";

interface KnowledgeTableProps {
  knowledgeList: KMSElement[];
}

const filterAndSortKnowledge = (
  knowledgeList: KMSElement[],
  searchQuery: string,
  sortConfig: { key: string; direction: string }
): KMSElement[] => {
  let filteredList = knowledgeList.filter((knowledge) =>
    (knowledge.file_name ?? knowledge.url ?? "")
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
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

    const getComparableValue = (item: KMSElement) => {
      if (sortConfig.key === "name") {
        return item.url ?? item.file_name;
      }
      if (sortConfig.key === "status") {
        return item.status;
      }

      return "";
    };

    filteredList = filteredList.sort((a, b) =>
      compareStrings(getComparableValue(a) ?? "", getComparableValue(b) ?? "")
    );
  }

  return filteredList;
};

const KnowledgeTable = React.forwardRef<HTMLDivElement, KnowledgeTableProps>(
  ({ knowledgeList }, ref) => {
    const [selectedKnowledge, setSelectedKnowledge] = useState<KMSElement[]>(
      []
    );
    const [lastSelectedIndex, setLastSelectedIndex] = useState<number | null>(
      null
    );
    const { onDeleteKnowledge } = useKnowledgeItem();
    const [allChecked, setAllChecked] = useState<boolean>(false);
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [filteredKnowledgeList, setFilteredKnowledgeList] =
      useState<KMSElement[]>(knowledgeList);
    const [allKnowledgeMode, setAllKnowledgeMode] = useState<boolean>(false);

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
      knowledge: KMSElement,
      index: number,
      event: React.MouseEvent
    ) => {
      const newSelectedKnowledge = updateSelectedItems<KMSElement>({
        item: knowledge,
        index,
        event,
        lastSelectedIndex,
        filteredList: filteredKnowledgeList,
        selectedItems: selectedKnowledge,
      });
      setSelectedKnowledge(newSelectedKnowledge.selectedItems);
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

    const isKnowledgeListEmpty =
      knowledgeList.filter((knowledge) => !knowledge.is_folder).length === 0;

    return (
      <div ref={ref} className={styles.knowledge_table_wrapper}>
        <div className={styles.content_header}>
          <span className={styles.title}>
            {allKnowledgeMode ? "My Knowledge" : "Uploaded Knowledge"}
          </span>
          <SwitchButton
            label="My Knowledge"
            checked={allKnowledgeMode}
            setChecked={setAllKnowledgeMode}
          />
        </div>
        {isKnowledgeListEmpty && !allKnowledgeMode && (
          <div className={styles.knowledge_tab_wrapper}>
            <MessageInfoBox type="warning">
              <div className={styles.message}>This brain is empty!</div>
            </MessageInfoBox>
          </div>
        )}
        <div className={styles.content}>
          {!allKnowledgeMode ? (
            <>
              {!isKnowledgeListEmpty && (
                <>
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
                          setSelectedKnowledge(
                            checked ? filteredKnowledgeList : []
                          );
                        }}
                      />
                      <div
                        className={styles.name}
                        onClick={() => handleSort("name")}
                      >
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
                </>
              )}
            </>
          ) : (
            <div className={styles.kms}>
              <KnowledgeManagementSystem fromBrainStudio={true} />
            </div>
          )}
        </div>
      </div>
    );
  }
);

KnowledgeTable.displayName = "KnowledgeTable";

export default KnowledgeTable;
