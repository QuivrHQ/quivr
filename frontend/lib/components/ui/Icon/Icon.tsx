import { IconType } from "react-icons/lib";

import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";
import { IconSize } from "@/lib/types/Icons";

import styles from "./Icon.module.scss";

interface IconProps {
  name: keyof typeof iconList;
  size: IconSize;
  color: Color;
  disabled?: boolean;
  classname?: string;
  hovered?: boolean;
}

export const Icon = ({
  name,
  size,
  color,
  disabled,
  classname,
  hovered,
}: IconProps): JSX.Element => {
  const IconComponent: IconType = iconList[name];

  return (
    <IconComponent
      className={`
      ${classname ?? ""} 
      ${styles[size] ?? ""} 
      ${styles[color] ?? ""}
      ${disabled ? styles.disabled ?? "" : ""}
      ${hovered ? styles.hovered ?? "" : ""}
      `}
    />
  );
};

export default Icon;
