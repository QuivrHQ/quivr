"use client";

import styles from "./ProcessLine.module.scss";

import { Process } from "../../types/process";

interface ProcessLineProps {
  process: Process;
  first?: boolean;
  last?: boolean;
}

const ProcessLine = ({
  process,
  first,
  last,
}: ProcessLineProps): JSX.Element => {
  return (
    <div
      className={`${styles.process_wrapper} ${
        first ? styles.first : last ? styles.last : ""
      }`}
    >
      {process.name}
    </div>
  );
};

export default ProcessLine;
