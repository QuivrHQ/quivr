import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./ConnectionButton.module.scss";

interface ConnectionButtonProps {
  label: string;
  index: number;
}

export const ConnectionButton = ({
  label,
  index,
}: ConnectionButtonProps): JSX.Element => {
  return (
    <div className={styles.connection_button_wrapper}>
      <div className={styles.left}>
        <ConnectionIcon letter={label[0]} index={index} />
        <span className={styles.label}>{label}</span>
      </div>
      <div className={styles.icons}>
        <Icon
          name="uploadFile"
          size="normal"
          color="black"
          handleHover={true}
        />
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
