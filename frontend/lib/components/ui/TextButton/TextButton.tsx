import { useState } from "react";

import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";

import styles from "./TextButton.module.scss";

import { Icon } from "../Icon/Icon";

interface TextButtonProps {
  iconName: keyof typeof iconList;
  label: string;
  color: Color;
}

export const TextButton = (props: TextButtonProps): JSX.Element => {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      className={styles.text_button_wrapper}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <Icon
        name={props.iconName}
        size="normal"
        color={props.color}
        hovered={hovered}
      />
      <span
        className={`
        ${styles[props.color] ?? ""}
        ${hovered ? styles.hovered ?? "" : ""}
        `}
      >
        {props.label}
      </span>
    </div>
  );
};

export default TextButton;
