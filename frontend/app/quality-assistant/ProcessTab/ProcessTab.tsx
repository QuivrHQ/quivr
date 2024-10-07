"use client";

import { useEffect, useState } from "react";

import { useAssistants } from "@/lib/api/assistants/useAssistants";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { filterAndSort, updateSelectedItems } from "@/lib/helpers/table";
import { useDevice } from "@/lib/hooks/useDevice";

import ProcessLine from "./Process/ProcessLine";
import styles from "./ProcessTab.module.scss";

import { Process } from "../types/process";

const ProcessTab = (): JSX.Element => {
  const [processes, setProcesses] = useState<Process[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedProcess, setSelectedProcess] = useState<Process[]>([]);
  const [allChecked, setAllChecked] = useState<boolean>(false);
  const [sortConfig, setSortConfig] = useState<{
    key: keyof Process;
    direction: "ascending" | "descending";
  }>({ key: "creation_time", direction: "descending" });
  const [filteredProcess, setFilteredProcess] = useState<Process[]>([]);
  const [lastSelectedIndex, setLastSelectedIndex] = useState<number | null>(
    null
  );
  const [loading, setLoading] = useState<boolean>(false);

  const { getTasks, deleteTask } = useAssistants();
  const { supabase } = useSupabase();
  const { isMobile } = useDevice();

  const loadTasks = async () => {
    try {
      const res = await getTasks();
      setProcesses(res);
      setFilteredProcess(res);
    } catch (error) {
      console.error(error);
    }
  };

  const handleStatusChange = () => {
    void loadTasks();
  };

  useEffect(() => {
    void loadTasks();
  }, []);

  useEffect(() => {
    const channel = supabase
      .channel("tasks")
      .on(
        "postgres_changes",
        { event: "UPDATE", schema: "public", table: "tasks" },
        handleStatusChange
      )
      .subscribe();

    return () => {
      void supabase.removeChannel(channel);
    };
  }, []);

  useEffect(() => {
    setFilteredProcess(
      filterAndSort(
        processes,
        searchQuery,
        sortConfig,
        (process) => process[sortConfig.key]
      )
    );
  }, [processes, searchQuery, sortConfig]);

  const handleDelete = async () => {
    setLoading(true);
    await Promise.all(
      selectedProcess.map(async (process) => await deleteTask(process.id))
    );

    const remainingProcesses = processes.filter(
      (process) =>
        !selectedProcess.some((selected) => selected.id === process.id)
    );

    setProcesses(remainingProcesses);
    setFilteredProcess(
      filterAndSort(
        remainingProcesses,
        searchQuery,
        sortConfig,
        (process) => process[sortConfig.key]
      )
    );

    setSelectedProcess([]);
    setAllChecked(false);
    setLoading(false);
  };

  const handleSelect = (
    process: Process,
    index: number,
    event: React.MouseEvent
  ) => {
    const newSelectedProcess = updateSelectedItems<Process>({
      item: process,
      index,
      event,
      lastSelectedIndex,
      filteredList: filteredProcess,
      selectedItems: selectedProcess,
    });
    setSelectedProcess(newSelectedProcess.selectedItems);
    setLastSelectedIndex(newSelectedProcess.lastSelectedIndex);
  };

  const handleSort = (key: keyof Process) => {
    setSortConfig((prevSortConfig) => {
      let direction: "ascending" | "descending" = "ascending";
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
    <div className={styles.process_tab_wrapper}>
      <span className={styles.title}>My Results</span>
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
          isLoading={loading}
        />
      </div>
      <div>
        <div
          className={`${styles.first_line}  ${!filteredProcess.length ? styles.empty : ""
            }`}
        >
          <div className={styles.left}>
            <Checkbox
              checked={allChecked}
              setChecked={(checked) => {
                setAllChecked(checked);
                setSelectedProcess(checked ? filteredProcess : []);
              }}
            />
            <div className={styles.left_fields}>
              <div
                className={`${styles.field} ${styles.assistant}`}
                onClick={() => handleSort("assistant_name")}
              >
                Assistant
                <div className={styles.icon}>
                  <Icon name="sort" size="small" color="black" />
                </div>
              </div>
              <div className={styles.field} onClick={() => handleSort("name")}>
                Files
                <div className={styles.icon}>
                  <Icon name="sort" size="small" color="black" />
                </div>
              </div>
            </div>
          </div>
          <div className={styles.right}>
            {!isMobile && (
              <>
                <div
                  className={styles.date}
                  onClick={() => handleSort("creation_time")}
                >
                  Date
                  <div className={styles.icon}>
                    <Icon name="sort" size="small" color="black" />
                  </div>
                </div>
                <div
                  className={styles.status}
                  onClick={() => handleSort("status")}
                >
                  Statut
                  <div className={styles.icon}>
                    <Icon name="sort" size="small" color="black" />
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
        <div className={styles.process_list}>
          {filteredProcess.map((process, index) => (
            <div key={process.id} className={styles.process_line}>
              <ProcessLine
                process={process}
                last={index === filteredProcess.length - 1}
                selected={selectedProcess.some(
                  (item) => item.id === process.id
                )}
                setSelected={(_selected, event) =>
                  handleSelect(process, index, event)
                }
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProcessTab;
