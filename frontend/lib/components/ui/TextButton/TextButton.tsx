import { useState } from "react";

import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";

import styles from "./TextButton.module.scss";

import { Icon } from "../Icon/Icon";

interface TextButtonProps {
  iconName?: keyof typeof iconList;
  label: string;
  color: Color;
  onClick?: () => void | Promise<void>;
  disabled?: boolean;
  small?: boolean;
}

export const TextButton = (props: TextButtonProps): JSX.Element => {
  const [hovered, setHovered] = useState<boolean>(false);

  return (
    <div
      className={`${styles.text_button_wrapper} ${
        props.disabled ? styles.disabled : ""
      } ${props.small ? styles.small : ""}`}
      onClick={props.onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {!!props.iconName && (
        <Icon
          name={props.iconName}
          size={props.small ? "small" : "normal"}
          color={hovered ? "primary" : props.color}
        />
      )}
      <span className={styles[props.color]}>{props.label}</span>
    </div>
  );
};

export default TextButton;
