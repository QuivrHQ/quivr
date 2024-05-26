import { useState } from "react";

import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
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
  important,
}: ButtonType): JSX.Element => {
  const [hovered, setHovered] = useState<boolean>(false);
  const { isDarkMode } = useUserSettingsContext();

  const handleClick = () => {
    if (onClick) {
      void onClick();
    }
  };

  const handleMouseEnter = () => {
    setHovered(true);
  };

  const handleMouseLeave = () => {
    setHovered(false);
  };

  const getIconColor = () => {
    if (hovered || (important && !disabled)) {
      return "white";
    } else if (disabled) {
      return "grey";
    } else {
      return color;
    }
  };

  return (
    <div
      className={`
      ${styles.button_wrapper} 
      ${styles[color]} 
      ${isDarkMode ? styles.dark : ""}
      ${hidden ? styles.hidden : ""}
      ${important ? styles.important : ""}
      ${disabled ? styles.disabled : ""}
      `}
      onClick={handleClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className={styles.icon_label}>
        {!isLoading ? (
          <Icon
            name={iconName}
            size="normal"
            color={getIconColor()}
            handleHover={false}
          />
        ) : (
          <LoaderIcon
            color={hovered || important ? "white" : disabled ? "grey" : color}
            size="small"
          />
        )}
        <span className={styles.label}>{label}</span>
      </div>
    </div>
  );
};

export default QuivrButton;
