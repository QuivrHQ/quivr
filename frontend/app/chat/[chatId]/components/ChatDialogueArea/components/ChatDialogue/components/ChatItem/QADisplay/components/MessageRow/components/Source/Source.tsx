import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./Source.module.scss";

import { SourceFile } from "../../types/types";

type SourceProps = {
  sourceFile: SourceFile;
  isSelected: boolean;
};
export const SourceCitations = ({
  sourceFile,
  isSelected,
}: SourceProps): JSX.Element => {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);

  return (
    <div className={styles.source_container}>
      <div
        className={`${styles.source_wrapper} ${
          isSelected ? styles.selected_source : ""
        }`}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className={styles.source_header}>
          <span className={styles.filename}>{sourceFile.filename}</span>
        </div>
      </div>
      <a
        onClick={(event) => event.stopPropagation()}
        href={sourceFile.file_url}
        target="_blank"
        rel="noopener noreferrer"
      >
        <Icon name="externLink" size="small" color="black" handleHover={true} />
      </a>
    </div>
  );
};
