import Image from "next/image";
import { useState } from "react";

import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";

import styles from "./Source.module.scss";

import { SourceFile } from "../../types/types";
import { CitationModal } from "../CitationModal/CitationModal";

type SourceProps = {
  sourceFile: SourceFile;
};
export const SourceCitations = ({ sourceFile }: SourceProps): JSX.Element => {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [hovered, isHovered] = useState<boolean>(false);
  const [isCitationModalOpened, setIsCitationModalOpened] =
    useState<boolean>(false);
  const [citationIndex, setCitationIndex] = useState<number>(0);
  const { integrationIconUrls } = useSync();

  return (
    <div>
      <div className={styles.source_and_citations_container}>
        <div
          className={styles.source_wrapper}
          onClick={() => setIsExpanded(!isExpanded)}
          onMouseEnter={() => isHovered(true)}
          onMouseLeave={() => isHovered(false)}
        >
          <a
            onClick={(event) => event.stopPropagation()}
            href={
              sourceFile.integration_link
                ? sourceFile.integration_link
                : sourceFile.file_url
            }
            target="_blank"
            rel="noopener noreferrer"
          >
            <div className={styles.source_header}>
              <span className={styles.filename}>{sourceFile.filename}</span>
              {sourceFile.integration ? (
                <Image
                  src={integrationIconUrls[sourceFile.integration]}
                  width="16"
                  height="16"
                  alt="integration_icon"
                />
              ) : (
                <Icon
                  name="externLink"
                  size="small"
                  color={hovered ? "primary" : "black"}
                />
              )}
            </div>
          </a>
        </div>
        <div className={styles.citations_container}>
          {sourceFile.citations.map((citation, i) => (
            <div key={i}>
              <Tooltip
                tooltip={citation
                  .split("Content:")
                  .slice(1)
                  .join("")
                  .replace(/\n{3,}/g, "\n\n")}
                small={true}
              >
                <span
                  className={styles.citation_index}
                  onClick={() => {
                    setIsCitationModalOpened(true);
                    setCitationIndex(i);
                  }}
                >
                  [{i + 1}]
                </span>
              </Tooltip>
            </div>
          ))}
        </div>
      </div>
      {isCitationModalOpened && (
        <CitationModal
          citation={sourceFile.citations[citationIndex]}
          sourceFile={sourceFile}
          isModalOpened={isCitationModalOpened}
          setIsModalOpened={setIsCitationModalOpened}
        />
      )}
    </div>
  );
};
