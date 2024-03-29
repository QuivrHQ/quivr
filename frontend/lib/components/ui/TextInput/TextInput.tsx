import styles from "./TextInput.module.scss";

import { Icon } from "../Icon/Icon";

type TextInputProps = {
  iconName?: string;
  label: string;
  inputValue: string;
  setInputValue?: (value: string) => void;
  simple?: boolean;
  onSubmit?: () => void;
  disabled?: boolean;
  crypted?: boolean;
};

export const TextInput = ({
  iconName,
  label,
  inputValue,
  setInputValue,
  simple,
  onSubmit,
  disabled,
  crypted,
}: TextInputProps): JSX.Element => {
  return (
    <div
      className={`
      ${styles.text_input_container} 
      ${simple ? styles.simple : ""}
      ${disabled ? styles.disabled : ""}
      `}
    >
      <input
        className={styles.text_input}
        type={crypted ? "password" : "text"}
        value={inputValue}
        onChange={(e) => setInputValue?.(e.target.value)}
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
