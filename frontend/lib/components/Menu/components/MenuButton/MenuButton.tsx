import { capitalCase } from "change-case";
import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { iconList } from "@/lib/helpers/iconList";

import styles from "./MenuButton.module.scss";

export interface ButtonProps {
  onClick?: () => void;
  label: string;
  iconName: keyof typeof iconList;
  type: "add" | "open";
  isSelected?: boolean;
  color: "gold" | "primary";
  parentHovered?: boolean;
}

export const MenuButton = (props: ButtonProps): JSX.Element => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={`
      ${styles.menu_button_wrapper} 
      ${props.isSelected ? styles.selected : ""}
      ${props.color === "gold" ? styles.gold : ""}
      `}
      onClick={props.onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={styles.left}>
        <Icon name={props.iconName} size="normal" color={props.color} />
        <span
          className={`
          ${styles.title} 
          ${
            props.color === "gold"
              ? styles.gold
              : isHovered || props.parentHovered
              ? styles.primary
              : ""
          }`}
        >
          {capitalCase(props.label)}
        </span>
      </div>
    </div>
  );
};
