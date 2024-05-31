import { useState } from "react";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./FolderLine.module.scss";

interface FolderLineProps {
  name: string;
  selectable: boolean;
}

export const FolderLine = ({
  name,
  selectable,
}: FolderLineProps): JSX.Element => {
  const [isCheckboxHovered, setIsCheckboxHovered] = useState(false);

  return (
    <div
      className={`${styles.folder_line_wrapper} ${
        isCheckboxHovered ? styles.no_hover : ""
      }`}
    >
      {selectable && (
        <div
          className={styles.checkbox_wrapper}
          onMouseEnter={() => setIsCheckboxHovered(true)}
          onMouseLeave={() => setIsCheckboxHovered(false)}
        >
          <Checkbox checked={false} setChecked={() => {}} />
        </div>
      )}
      <Icon name="folder" color="black" size="normal" />
      <span className={styles.folder_name}>{name}</span>
    </div>
  );
};
