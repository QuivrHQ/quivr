"use client";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";

import styles from "./ProcessLine.module.scss";

import { Process } from "../../types/process";

interface ProcessLineProps {
  process: Process;
  last?: boolean;
  selected: boolean;
  setSelected: (selected: boolean, event: React.MouseEvent) => void;
}

const ProcessLine = ({
  process,
  last,
  selected,
  setSelected,
}: ProcessLineProps): JSX.Element => {
  return (
    <div className={`${styles.process_wrapper} ${last ? styles.last : ""}`}>
      <div className={styles.left}>
        <Checkbox
          checked={selected}
          setChecked={(checked, event) => setSelected(checked, event)}
        />
        <span className={styles.name}>{process.name}</span>
      </div>
    </div>
  );
};

export default ProcessLine;
