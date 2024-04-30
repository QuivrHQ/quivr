import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./Citation.module.scss";

import { CitationType } from "../../types/types";

type CitationProps = {
  citation: CitationType;
};
export const Citation = ({ citation }: CitationProps): JSX.Element => {
  const [folded, setFolded] = useState<boolean>(true);

  return (
    <div
      className={`${styles.citation_wrapper} ${!folded ? styles.unfolded : ""}`}
      onClick={() => setFolded(!folded)}
    >
      <div className={styles.citation_header}>
        <span>{citation.filename}</span>
        <Icon
          name={folded ? "unfold" : "fold"}
          size="normal"
          color="black"
          handleHover={true}
        />
      </div>
      <div className={styles.citation_content}>{citation.citation}</div>
    </div>
  );
};
