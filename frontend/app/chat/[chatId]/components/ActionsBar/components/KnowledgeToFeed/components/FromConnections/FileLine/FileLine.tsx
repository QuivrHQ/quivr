import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./FileLine.module.scss";

interface FileLineProps {
  name: string;
}

export const FileLine = ({ name }: FileLineProps): JSX.Element => {
  return (
    <div className={styles.file_line_wrapper}>
      <Icon name="file" color="black" size="small" />
      <span className={styles.file_name}>{name}</span>
    </div>
  );
};
