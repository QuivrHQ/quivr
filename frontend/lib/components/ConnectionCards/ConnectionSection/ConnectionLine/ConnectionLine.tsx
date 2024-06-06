import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./ConnectionLine.module.scss";

interface ConnectionLineProps {
  label: string;
  index: number;
}

export const ConnectionLine = ({
  label,
  index,
}: ConnectionLineProps): JSX.Element => {
  return (
    <div className={styles.connection_line_wrapper}>
      <div className={styles.left}>
        <ConnectionIcon letter={label[0]} index={index} />
        <span className={styles.label}>{label}</span>
      </div>
      <div className={styles.icons}>
        <Icon
          name="delete"
          size="normal"
          color="dangerous"
          handleHover={true}
        />
      </div>
    </div>
  );
};
