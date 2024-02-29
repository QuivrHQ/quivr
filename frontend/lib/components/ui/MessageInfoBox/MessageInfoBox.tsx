import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";

import styles from "./MessageInfoBox.module.scss";

import { Icon } from "../Icon/Icon";

export type MessageInfoBoxProps = {
  children: React.ReactNode;
  type: "info" | "success" | "warning" | "error";
};

export const MessageInfoBox = ({
  children,
  type,
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
      default:
        return { iconName: "info", iconColor: "primary" };
    }
  };

  return (
    <div className={`${styles.message_info_box_wrapper} ${styles[type]} `}>
      <Icon
        name={getIconProps().iconName}
        size="normal"
        color={getIconProps().iconColor}
      />
      {children}
    </div>
  );
};
