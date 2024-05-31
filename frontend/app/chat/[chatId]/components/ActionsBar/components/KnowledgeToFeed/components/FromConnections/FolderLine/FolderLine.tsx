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
  return (
    <div className={styles.folder_line_wrapper}>
      {selectable && <Checkbox checked={false} setChecked={() => {}} />}
      <Icon name="folder" color="black" size="normal" />
      <span className={styles.folder_name}>{name}</span>
    </div>
  );
};
