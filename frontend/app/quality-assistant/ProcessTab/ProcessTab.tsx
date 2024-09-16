"use client";

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
  return (
    <div className={styles.process_tab_wrapper}>
      <span className={styles.title}>Uploaded knowledge</span>
      <div className={styles.process_list}>
        {mockProcesses.map((process, index) => (
          <div key={process.id} className={styles.process_line}>
            <ProcessLine
              process={process}
              first={index === 0}
              last={index === mockProcesses.length - 1}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProcessTab;
