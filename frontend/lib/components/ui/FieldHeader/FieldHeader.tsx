import styles from "./FieldHeader.module.scss";

import { Icon } from "../Icon/Icon";

type FieldHeaderProps = {
  iconName: string;
  label: string;
};

export const FieldHeader = ({
  iconName,
  label,
}: FieldHeaderProps): JSX.Element => {
  return (
    <div className={styles.field_header_wrapper}>
      <Icon name={iconName} color="black" size="small" />
      <label>{label}</label>
    </div>
  );
};
