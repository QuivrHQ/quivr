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
}: ButtonType): JSX.Element => {
  const [hovered, setHovered] = useState<boolean>(false);

  return (
    <div
      className={`${styles.button_wrapper} ${styles[color]}`}
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {!isLoading ? (
        <div className={styles.icon_label}>
          <Icon
            name={iconName}
            size="normal"
            color={hovered ? "white" : color}
            handleHover={false}
          />
          <span className={styles.label}>{label}</span>
        </div>
      ) : (
        <LoaderIcon color="black" size="small" />
      )}
    </div>
  );
};

export default QuivrButton;
