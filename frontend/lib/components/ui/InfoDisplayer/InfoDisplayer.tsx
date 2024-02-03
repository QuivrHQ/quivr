import styles from "./InfoDisplayer.module.scss";

import { Icon } from "../Icon/Icon";

type InfoDisplayerProps = {
  iconName: string;
  label: string;
  children: React.ReactNode;
};

export const InfoDisplayer = ({
  iconName,
  label,
  children,
}: InfoDisplayerProps): JSX.Element => {
  return (
    <div className={styles.info_displayer_container}>
      <div className={styles.header}>
        <Icon name={iconName} color="black" size="small" />
        <label>{label}</label>
      </div>
      {children}
    </div>
  );
};
