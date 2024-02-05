import { Button } from "@/lib/types/QuivrButton";

import styles from "./QuivrButton.module.scss";

export const QuivrButton = ({ button }: { button: Button }): JSX.Element => {
  return (
    <div className={`${styles.button_wrapper} ${styles[button.color]}`}>
      {button.label}
    </div>
  );
};

export default QuivrButton;
