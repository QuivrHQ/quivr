import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";

import styles from "./MessageInfoBox.module.scss";

import { Icon } from "../Icon/Icon";

export type MessageInfoBoxProps = {
  children: React.ReactNode;
  type: "info" | "success" | "warning" | "error" | "tutorial";
  unforceWhite?: boolean;
};

export const MessageInfoBox = ({
  children,
  type,
  unforceWhite,
}: MessageInfoBoxProps): JSX.Element => {
  const getIconProps = (): {
    iconName: keyof typeof iconList;
    iconColor: Color;
  } => {
    switch (type) {
      case "info":
        return { iconName: "info", iconColor: "primary" };
      case "success":
        return { iconName: "check", iconColor: "success" };
      case "warning":
        return { iconName: "warning", iconColor: "warning" };
      case "tutorial":
        return { iconName: "step", iconColor: "gold" };
      default:
        return { iconName: "info", iconColor: "primary" };
    }
  };

  const { isDarkMode } = useUserSettingsContext();

  return (
    <div
      className={`${styles.message_info_box_wrapper} ${styles[type]} ${
        isDarkMode && !unforceWhite ? styles.dark : ""
      }`}
    >
      <Icon
        name={getIconProps().iconName}
        size="normal"
        color={getIconProps().iconColor}
      />
      {children}
    </div>
  );
};
