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
  onKeyDown?: (event: React.KeyboardEvent) => void;
  small?: boolean;
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
  onKeyDown,
  small,
}: TextInputProps): JSX.Element => {
  return (
    <div
      className={`
      ${styles.text_input_container} 
      ${simple ? styles.simple : ""}
      ${disabled ? styles.disabled : ""}
      ${small ? styles.small : ""}
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
          onKeyDown?.(e);
        }}
      />
      {!simple && iconName && (
        <Icon
          name={iconName}
          size={small ? "small" : "normal"}
          color={onSubmit ? (inputValue ? "accent" : "grey") : "black"}
          onClick={onSubmit}
        />
      )}
    </div>
  );
};
