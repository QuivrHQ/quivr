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
  gold?: boolean;
}

export const MenuButton = (props: ButtonProps): JSX.Element => {
  return (
    <div
      className={`
      ${styles.menu_button_wrapper} 
      ${props.isSelected ? styles.selected : ""}
      ${props.gold ? styles.gold : ""}
      `}
      onClick={props.onClick}
    >
      <div className={styles.left}>
        <Icon
          name={props.iconName}
          size="normal"
          color={props.gold ? "gold" : "accent"}
        />
        <span className={styles.title}>{capitalCase(props.label)}</span>
      </div>
      <Icon
        name={props.type === "add" ? "addWithoutCircle" : "chevronRight"}
        size="large"
        color={props.gold ? "gold" : "accent"}
      />
    </div>
  );
};
