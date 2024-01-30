import { capitalCase } from "change-case";

import Icon from "@/lib/components/ui/Icon/Icon";
import { iconList } from "@/lib/helpers/iconList";

import styles from "./MenuButton.module.scss";

export interface ButtonProps {
  onClick?: () => void;
  label: string;
  iconName: keyof typeof iconList;
  type: "add" | "open";
  isSelected?: boolean;
}

export const MenuButton = (props: ButtonProps): JSX.Element => {
  return (
    <div
      className={`
      ${styles.menu_button_wrapper} 
      ${props.isSelected ? styles.selected : ""}
      `}
    >
      <div className={styles.left}>
        <Icon name={props.iconName} size="normal" color="accent" />
        <span className={styles.title}>{capitalCase(props.label)}</span>
      </div>
      <Icon
        name={props.type === "add" ? "add" : "chevronRight"}
        size="large"
        color="accent"
      />
    </div>
  );
};
