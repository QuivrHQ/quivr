"use client";

import { capitalCase } from "change-case";
import format from "date-fns/format";
import { fr } from "date-fns/locale";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import { Tag } from "@/lib/components/ui/Tag/Tag";
import { useDevice } from "@/lib/hooks/useDevice";

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
  const [showResult, setShowResult] = useState(false);
  const { isMobile } = useDevice();

  console.info(process.result);

  return (
    <>
      <div
        className={`${styles.process_wrapper} ${last ? styles.last : ""} ${
          process.status === "completed" ? styles.clickable : ""
        }`}
        onClick={() => {
          if (process.status === "completed") {
            setShowResult(!showResult);
          }
        }}
      >
        <div className={styles.left}>
          <Checkbox
            checked={selected}
            setChecked={(checked, event) => setSelected(checked, event)}
          />
          <span className={styles.name}>{process.name}</span>
        </div>
        <div className={styles.right}>
          {!isMobile && (
            <>
              <span className={styles.date}>
                {format(new Date(process.datetime), " d MMMM yyyy '-' HH:mm", {
                  locale: fr,
                })}
              </span>
              <div className={styles.status}>
                <Tag
                  name={capitalCase(process.status)}
                  color={
                    process.status === "error"
                      ? "dangerous"
                      : process.status === "processing"
                      ? "primary"
                      : process.status === "completed"
                      ? "success"
                      : "grey"
                  }
                />
              </div>
            </>
          )}
          <Icon
            name={
              process.status === "completed"
                ? "download"
                : process.status === "error"
                ? "warning"
                : "waiting"
            }
            size="normal"
            color="black"
            handleHover={process.status === "completed"}
          />
        </div>
      </div>

      <Modal
        size="big"
        isOpen={showResult}
        setOpen={setShowResult}
        CloseTrigger={<div />}
      >
        <div className={styles.markdown}>
          <ReactMarkdown remarkPlugins={[gfm]}>
            {process.result.replace(/\n/g, "\n")}
          </ReactMarkdown>
        </div>
      </Modal>
    </>
  );
};

export default ProcessLine;
