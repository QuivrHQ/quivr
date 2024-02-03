import styles from "./TextInput.module.scss";

import { FieldHeader } from "../FieldHeader/FieldHeader";

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
      <FieldHeader iconName={iconName} label={label} />
      <input
        className={styles.text_input}
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
    </div>
  );
};
