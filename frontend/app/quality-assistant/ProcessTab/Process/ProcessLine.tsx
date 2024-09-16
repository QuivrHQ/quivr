"use client";

import styles from "./ProcessLine.module.scss";

import { Process } from "../../types/process";

interface ProcessLineProps {
  process: Process;
  last?: boolean;
}

const ProcessLine = ({ process, last }: ProcessLineProps): JSX.Element => {
  return (
    <div className={`${styles.process_wrapper} ${last ? styles.last : ""}`}>
      {process.name}
    </div>
  );
};

export default ProcessLine;
