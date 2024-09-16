"use client";

import { useState } from "react";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { useDevice } from "@/lib/hooks/useDevice";

import ProcessLine from "./Process/ProcessLine";
import styles from "./ProcessTab.module.scss";

import { Process } from "../types/process";

const mockProcesses: Process[] = [
  {
    id: 1,
    name: "Process 1",
    datetime: new Date().toISOString(),
    status: "pending",
  },
  {
    id: 2,
    name: "Process 2",
    datetime: new Date(Date.now() - 86400000 * 1).toISOString(),
    status: "processing",
  },
  {
    id: 3,
    name: "Process 3",
    datetime: new Date(Date.now() - 86400000 * 2).toISOString(),
    status: "completed",
  },
  {
    id: 4,
    name: "Process 4",
    datetime: new Date(Date.now() - 86400000 * 3).toISOString(),
    status: "error",
  },
  {
    id: 5,
    name: "Process 5",
    datetime: new Date(Date.now() - 86400000 * 4).toISOString(),
    status: "pending",
  },
  {
    id: 6,
    name: "Process 6",
    datetime: new Date(Date.now() - 86400000 * 5).toISOString(),
    status: "processing",
  },
  {
    id: 7,
    name: "Process 7",
    datetime: new Date(Date.now() - 86400000 * 6).toISOString(),
    status: "completed",
  },
];

const ProcessTab = (): JSX.Element => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedProcess, setSelectedProcess] = useState<Process[]>([]);

  const { isMobile } = useDevice();

  const handleDelete = () => {
    console.info("delete");
  };

  const filteredProcesses = mockProcesses.filter((process) =>
    process.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className={styles.process_tab_wrapper}>
      <span className={styles.title}>Mes Résultats</span>
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
          disabled={selectedProcess.length === 0}
          onClick={handleDelete}
        />
      </div>
      <div>
        <div className={styles.first_line}>
          <div className={styles.left}>
            {/* <Checkbox
            checked={allChecked}
            setChecked={(checked) => {
              setAllChecked(checked);
              setSelectedKnowledge(checked ? filteredKnowledgeList : []);
            }}
          /> */}
            <div className={styles.name}>
              Name
              <div className={styles.icon}>
                <Icon name="sort" size="small" color="black" />
              </div>
            </div>
          </div>
          <div className={styles.right}>
            {!isMobile && (
              <div className={styles.status}>
                Status
                <div className={styles.icon}>
                  <Icon name="sort" size="small" color="black" />
                </div>
              </div>
            )}
            <span className={styles.actions}>Actions</span>
          </div>
        </div>
        <div className={styles.process_list}>
          {filteredProcesses.map((process, index) => (
            <div key={process.id} className={styles.process_line}>
              <ProcessLine
                process={process}
                last={index === filteredProcesses.length - 1}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProcessTab;
