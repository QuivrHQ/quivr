import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

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
      <div className={styles.button_wrapper}>
        <QuivrButton
          label="Use"
          small={true}
          iconName="chevronRight"
          color="primary"
        />
      </div>
    </div>
  );
};
