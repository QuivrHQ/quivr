import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";

import styles from "./TextButton.module.scss";

import { Icon } from "../Icon/Icon";

interface TextButtonProps {
  iconName?: keyof typeof iconList;
  label: string;
  color: Color;
  onClick?: () => void;
  disabled?: boolean;
}

export const TextButton = (props: TextButtonProps): JSX.Element => {
  return (
    <div
      className={`${styles.text_button_wrapper} ${
        props.disabled ? styles.disabled : ""
      }`}
      onClick={props.onClick}
    >
      {!!props.iconName && (
        <Icon name={props.iconName} size="normal" color={props.color} />
      )}
      <span className={styles[props.color]}>{props.label}</span>
    </div>
  );
};

export default TextButton;
