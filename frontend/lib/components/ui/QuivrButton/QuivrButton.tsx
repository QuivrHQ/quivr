import { useState } from "react";

import { ButtonType } from "@/lib/types/QuivrButton";

import styles from "./QuivrButton.module.scss";

import { Icon } from "../Icon/Icon";
import { LoaderIcon } from "../LoaderIcon/LoaderIcon";

export const QuivrButton = ({
  onClick,
  label,
  color,
  isLoading,
  iconName,
  disabled,
  hidden,
}: ButtonType): JSX.Element => {
  const [hovered, setHovered] = useState<boolean>(false);

  return (
    <div
      className={`
      ${styles.button_wrapper} 
      ${styles[color]} 
      ${disabled ? styles.disabled : ""}
      ${hidden ? styles.hidden : ""}
      `}
      // eslint-disable-next-line @typescript-eslint/no-misused-promises
      onClick={() => onClick?.()}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className={styles.icon_label}>
        {!isLoading ? (
          <Icon
            name={iconName}
            size="normal"
            color={hovered ? "white" : disabled ? "grey" : color}
            handleHover={false}
          />
        ) : (
          <LoaderIcon
            color={hovered ? "white" : disabled ? "grey" : color}
            size="small"
          />
        )}
        <span className={styles.label}>{label}</span>
      </div>
    </div>
  );
};

export default QuivrButton;
