import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";

import styles from "./MessageInfoBox.module.scss";

import { Icon } from "../Icon/Icon";

export type MessageInfoBoxProps = {
  content: string;
  type: "info" | "success" | "warning" | "error";
};

export const MessageInfoBox = ({
  content,
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
      <span>{content}</span>
    </div>
  );
};
