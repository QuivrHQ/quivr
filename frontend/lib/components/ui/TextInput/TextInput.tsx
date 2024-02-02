import styles from "./TextInput.module.scss";

import { Icon } from "../Icon/Icon";

type TextInputProps = {
  iconName: string;
  label: string;
  inputValue: string;
  setInputValue: (value: string) => void;
};

export const TextInput = ({
  iconName,
  label,
  inputValue,
  setInputValue,
}: TextInputProps): JSX.Element => {
  return (
    <div className={styles.text_input_container}>
      <div className={styles.input_header}>
        <Icon name={iconName} color="black" size="small" />
        <label>{label}</label>
      </div>
      <input
        className={styles.text_input}
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
    </div>
  );
};
