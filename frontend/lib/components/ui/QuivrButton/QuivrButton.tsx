import { ButtonType } from "@/lib/types/QuivrButton";

import styles from "./QuivrButton.module.scss";

import { LoaderIcon } from "../LoaderIcon/LoaderIcon";

export const QuivrButton = ({
  button,
}: {
  button: ButtonType;
}): JSX.Element => {
  return (
    <div
      className={`${styles.button_wrapper} ${styles[button.color]}`}
      onClick={button.onClick}
    >
      {!button.isLoading ? (
        <span>button.label </span>
      ) : (
        <LoaderIcon color="white" size="small" />
      )}
    </div>
  );
};

export default QuivrButton;
