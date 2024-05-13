import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./Citation.module.scss";

type CitationProps = {
  citation: string;
};
export const Citation = ({ citation }: CitationProps): JSX.Element => {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);

  const contentIndex = citation.indexOf("Content:");
  let cleanedCitation, content;

  if (contentIndex !== -1) {
    cleanedCitation = citation.substring(contentIndex);
    [, content] = cleanedCitation.split("Content:");
  } else {
    content = citation;
  }

  const handleIconClick = (event: React.MouseEvent) => {
    event.stopPropagation();
    setIsExpanded(!isExpanded);
  };

  return (
    <div
      className={styles.citation_wrapper}
      onClick={(event) => handleIconClick(event)}
    >
      <div className={styles.citation_header}>
        <span
          className={`${styles.citation} ${!isExpanded ? styles.folded : ""}`}
        >
          {content}
        </span>
        <div className={styles.icon}>
          <Icon
            name={isExpanded ? "fold" : "unfold"}
            size="normal"
            color="black"
            handleHover={true}
          />
        </div>
      </div>
    </div>
  );
};
