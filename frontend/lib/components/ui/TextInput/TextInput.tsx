import styles from "./TextInput.module.scss";

import { Icon } from "../Icon/Icon";

type TextInputProps = {
  iconName?: string;
  label: string;
  inputValue: string;
  setInputValue: (value: string) => void;
  simple?: boolean;
  onSubmit?: () => void;
};

export const TextInput = ({
  iconName,
  label,
  inputValue,
  setInputValue,
  simple,
  onSubmit,
}: TextInputProps): JSX.Element => {
  return (
    <div
      className={`
      ${styles.text_input_container} 
      ${simple ? styles.simple : ""}
      `}
    >
      <input
        className={styles.text_input}
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder={label}
        onKeyDown={(e) => {
          if (e.key === "Enter" && onSubmit) {
            onSubmit();
          }
        }}
      />
      {!simple && iconName && (
        <Icon
          name={iconName}
          size="normal"
          color={onSubmit ? (inputValue ? "accent" : "grey") : "black"}
          onClick={onSubmit}
        />
      )}
    </div>
  );
};
