import styles from "./InfoDisplayer.module.scss";

import { FieldHeader } from "../FieldHeader/FieldHeader";

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
      <FieldHeader iconName={iconName} label={label} />
      {children}
    </div>
  );
};
