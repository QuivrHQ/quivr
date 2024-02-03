import styles from "./CountrySelector.module.scss";

import { FieldHeader } from "../FieldHeader/FieldHeader";

type CountrySelectorProps = {
  iconName: string;
  label: string;
};

export const CountrySelector = ({
  iconName,
  label,
}: CountrySelectorProps): JSX.Element => {
  return (
    <div className={styles.text_input_container}>
      <FieldHeader iconName={iconName} label={label} />
    </div>
  );
};
