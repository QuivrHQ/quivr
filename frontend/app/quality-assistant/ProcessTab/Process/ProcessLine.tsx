"use client";

import styles from "./ProcessLine.module.scss";

import { Process } from "../../types/process";

const ProcessLine = ({ process }: { process: Process }): JSX.Element => {
  return <div className={styles.process_wrapper}>{process.name}</div>;
};

export default ProcessLine;
