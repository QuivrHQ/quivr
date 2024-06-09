import styles from "./SwitchButton.module.scss";

interface SwitchButtonProps {
  label: string;
  checked: boolean;
  setChecked: (checked: boolean) => void;
}

export const SwitchButton = ({
  label,
  checked,
  setChecked,
}: SwitchButtonProps): JSX.Element => {
  const handleToggle = () => {
    setChecked(!checked);
  };

  return (
    <div className={styles.switch_wrapper}>
      <span>{label}</span>
      <div
        className={`${styles.slider} ${checked ? styles.checked : ""}`}
        onClick={handleToggle}
      >
        <div className={styles.slider_bubble}></div>
      </div>
    </div>
  );
};

export default SwitchButton;
