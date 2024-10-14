import { useState } from "react";

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
  url?: boolean;
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
  url,
}: TextInputProps): JSX.Element => {
  const [warning, setWarning] = useState<string>("");

  const isValidUrl = (value: string): boolean => {
    try {
      new URL(value);

      return true;
    } catch (_) {
      return false;
    }
  };

  const handleSubmit = () => {
    if (!url || isValidUrl(inputValue)) {
      setWarning("");
      onSubmit?.();
    } else {
      setWarning("Please enter a valid URL.");
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue?.(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
    onKeyDown?.(e);
  };

  const getIconColor = () => {
    if (!inputValue) {
      return "grey";
    }
    if (url) {
      return isValidUrl(inputValue) ? "accent" : "grey";
    }

    return "accent";
  };

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
        onChange={handleInputChange}
        placeholder={label}
        onKeyDown={handleKeyDown}
      />
      {warning && !isValidUrl(inputValue) && (
        <div className={styles.warning}>{warning}</div>
      )}
      {!simple && iconName && (
        <Icon
          name={iconName}
          size={small ? "small" : "normal"}
          color={getIconColor()}
          onClick={handleSubmit}
        />
      )}
    </div>
  );
};
