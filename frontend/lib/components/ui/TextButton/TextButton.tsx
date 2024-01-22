import { useState } from "react";

import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";

import { Icon } from "../Icon/Icon";

import styles from "./TextButton.module.scss";

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
      <span
        className={`
        ${styles[props.color] ?? ""}
        ${hovered ? styles.hovered ?? "" : ""}
        `}
      >
        {props.label}
      </span>
      <Icon
        name={props.iconName}
        size="normal"
        color={props.color}
        hovered={hovered}
      />
    </div>
  );
};

export default TextButton;
