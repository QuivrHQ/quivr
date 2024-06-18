import { Modal } from "@/lib/components/ui/Modal/Modal";

import styles from "./CitationModal.module.scss";

import { SourceFile } from "../../types/types";

type CitationModalProps = {
  citation: string;
  sourceFile: SourceFile;
  isModalOpened: boolean;
  setIsModalOpened: (isModalOpened: boolean) => void;
};
export const CitationModal = ({
  citation,
  sourceFile,
  isModalOpened,
  setIsModalOpened,
}: CitationModalProps): JSX.Element => {
  return (
    <Modal
      isOpen={isModalOpened}
      setOpen={setIsModalOpened}
      CloseTrigger={<div />}
    >
      <div className={styles.modal_wrapper}>
        <div className={styles.title_wrapper}>
          <span className={styles.title}>Text extract from:</span>
          <a
            href={sourceFile.file_url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.file_link}
          >
            <span className={styles.filename}>{sourceFile.filename}</span>
          </a>
        </div>
        <span className={styles.citation}>
          {citation
            .split("Content:")
            .slice(1)
            .join("")
            .replace(/\n{3,}/g, "\n\n")}
        </span>
      </div>
    </Modal>
  );
};
