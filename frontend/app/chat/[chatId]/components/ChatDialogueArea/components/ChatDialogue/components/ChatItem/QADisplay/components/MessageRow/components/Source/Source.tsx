import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";

import styles from "./Source.module.scss";

import { SourceFile } from "../../types/types";

type SourceProps = {
  sourceFile: SourceFile;
};
export const SourceCitations = ({ sourceFile }: SourceProps): JSX.Element => {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [hovered, isHovered] = useState<boolean>(false);

  return (
    <div className={styles.source_and_citations_container}>
      <div
        className={styles.source_wrapper}
        onClick={() => setIsExpanded(!isExpanded)}
        onMouseEnter={() => isHovered(true)}
        onMouseLeave={() => isHovered(false)}
      >
        <a
          onClick={(event) => event.stopPropagation()}
          href={sourceFile.file_url}
          target="_blank"
          rel="noopener noreferrer"
        >
          <div className={styles.source_header}>
            <span className={styles.filename}>{sourceFile.filename}</span>
            <Icon
              name="externLink"
              size="small"
              color={hovered ? "primary" : "black"}
            />
          </div>
        </a>
      </div>
      <div className={styles.citations_container}>
        {sourceFile.citations.map((citation, i) => (
          <div key={i}>
            <Tooltip tooltip={citation} small={true}>
              <span className={styles.citation_index}>[{i + 1}]</span>
            </Tooltip>
          </div>
        ))}
      </div>
    </div>
  );
};
