import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./FileLine.module.scss";

interface FileLineProps {
  name: string;
  selectable: boolean;
}

export const FileLine = ({ name, selectable }: FileLineProps): JSX.Element => {
  return (
    <div className={styles.file_line_wrapper}>
      {selectable && <Checkbox checked={false} setChecked={() => {}} />}
      <Icon name="file" color="black" size="small" />
      <span className={styles.file_name}>{name}</span>
    </div>
  );
};
