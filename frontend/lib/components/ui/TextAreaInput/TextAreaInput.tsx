import styles from "./TextAreaInput.module.scss";

type TextAreaInputProps = {
  label: string;
  inputValue: string;
  setInputValue: (value: string) => void;
  onSubmit?: () => void;
};

export const TextAreaInput = ({
  label,
  inputValue,
  setInputValue,
  onSubmit,
}: TextAreaInputProps): JSX.Element => {
  return (
    <div className={styles.text_area_input_container}>
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
