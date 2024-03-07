import styles from "./TextAreaInput.module.scss";

type TextAreaInputProps = {
  label: string;
  inputValue: string;
  setInputValue: (value: string) => void;
  onSubmit?: () => void;
  disabled?: boolean;
};

export const TextAreaInput = ({
  label,
  inputValue,
  setInputValue,
  onSubmit,
  disabled,
}: TextAreaInputProps): JSX.Element => {
  return (
    <div
      className={`${styles.text_area_input_container} ${
        disabled ? styles.disabled : ""
      }`}
    >
      <textarea
        className={styles.text_area_input}
        value={inputValue}
        rows={5}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder={label}
        onKeyDown={(e) => {
          if (e.key === "Enter" && onSubmit) {
            onSubmit();
          }
        }}
      />
    </div>
  );
};
