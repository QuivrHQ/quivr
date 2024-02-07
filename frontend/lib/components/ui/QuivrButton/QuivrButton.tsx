import { ButtonType } from "@/lib/types/QuivrButton";

import styles from "./QuivrButton.module.scss";

import { LoaderIcon } from "../LoaderIcon/LoaderIcon";

export const QuivrButton = ({
  onClick,
  label,
  color,
  isLoading,
}: ButtonType): JSX.Element => {
  return (
    <div
      className={`${styles.button_wrapper} ${styles[color]}`}
      onClick={onClick}
    >
      {!isLoading ? (
        <span>{label}</span>
      ) : (
        <LoaderIcon color="black" size="small" />
      )}
    </div>
  );
};

export default QuivrButton;
