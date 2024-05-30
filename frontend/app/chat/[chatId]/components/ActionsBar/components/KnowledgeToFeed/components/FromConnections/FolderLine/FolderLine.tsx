import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./FolderLine.module.scss";

interface FolderLineProps {
  name: string;
  selectable: boolean;
}

export const FolderLine = ({ name }: FolderLineProps): JSX.Element => {
  return (
    <div className={styles.folder_line_wrapper}>
      <Icon name="folder" color="black" size="normal" />
      <span className={styles.folder_name}>{name}</span>
    </div>
  );
};
