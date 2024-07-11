import { useState } from "react";

import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { ButtonType } from "@/lib/types/QuivrButton";

import styles from "./QuivrButton.module.scss";

import { Icon } from "../Icon/Icon";
import { LoaderIcon } from "../LoaderIcon/LoaderIcon";
import Tooltip from "../Tooltip/Tooltip";

export const QuivrButton = ({
  onClick,
  label,
  color,
  isLoading,
  iconName,
  disabled,
  hidden,
  important,
  small,
  tooltip,
}: ButtonType): JSX.Element => {
  const [hovered, setHovered] = useState<boolean>(false);
  const { isDarkMode } = useUserSettingsContext();

  const handleMouseEnter = () => setHovered(true);
  const handleMouseLeave = () => setHovered(false);

  const handleClick = () => {
    if (!disabled) {
      void onClick?.();
    }
  };

  const useIconColor = () => {
    if ((hovered && !disabled) || (important && !disabled)) {
      return "white";
    }
    if (disabled) {
      return "grey";
    }

    return color;
  };

  const iconColor = useIconColor();

  const buttonClasses = `${styles.button_wrapper} ${styles[color]} ${
    isDarkMode ? styles.dark : ""
  } ${hidden ? styles.hidden : ""} ${important ? styles.important : ""} ${
    disabled ? styles.disabled : ""
  } ${small ? styles.small : ""}`;

  const ButtonContent = (
    <div
      className={buttonClasses}
      onClick={handleClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className={styles.icon_label}>
        {!isLoading ? (
          <Icon
            name={iconName}
            size={small ? "small" : "normal"}
            color={iconColor}
            handleHover={false}
          />
        ) : (
          <LoaderIcon color={iconColor} size={small ? "small" : "normal"} />
        )}
        <span className={styles.label}>{label}</span>
      </div>
    </div>
  );

  return disabled ? (
    <Tooltip tooltip={tooltip}>{ButtonContent}</Tooltip>
  ) : (
    ButtonContent
  );
};

export default QuivrButton;
