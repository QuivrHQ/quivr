import { useEffect, useState } from "react";

import styles from "./Checkbox.module.scss";

interface CheckboxProps {
  label: string;
  checked: boolean;
  setChecked: (value: boolean) => void;
}

export const Checkbox = ({
  label,
  checked,
  setChecked,
}: CheckboxProps): JSX.Element => {
  const [currentChecked, setCurrentChecked] = useState<boolean>(checked);

  useEffect(() => {
    setCurrentChecked(checked);
  }, [checked]);

  return (
    <div
      className={styles.checkbox_wrapper}
      onClick={() => {
        setChecked(!currentChecked);
        setCurrentChecked(!currentChecked);
      }}
    >
      <div
        className={`${styles.checkbox} ${currentChecked ? styles.filled : ""}`}
      ></div>
      <span>{label}</span>
    </div>
  );
};
