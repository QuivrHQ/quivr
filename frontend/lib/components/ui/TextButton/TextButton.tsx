import { iconList } from "@/lib/helpers/iconList";
import { Color } from "@/lib/types/Colors";

import { Icon } from "../Icon/Icon";

import styles from "./TextButton.module.scss";

interface TextButtonProps {
  name: keyof typeof iconList;
  label: string;
  color: Color;
}

export const TextButton = (props: TextButtonProps): JSX.Element => {
  return (
    <div className={styles.text_button_wrapper}>
      <Icon name={props.name} size="normal" color={props.color} />
      <span>{props.label}</span>
    </div>
  );
};

export default TextButton;
