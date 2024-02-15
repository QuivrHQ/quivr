import { Option } from "@/lib/types/Options";

import styles from "./OptionsModal.module.scss";

import { Icon } from "../Icon/Icon";

type OptionsModalProps = {
  options: Option[];
};

export const OptionsModal = ({ options }: OptionsModalProps): JSX.Element => {
  return (
    <div className={styles.options_modal_wrapper}>
      {options.map((option, index) => (
        <div className={styles.option} key={index} onClick={option.onClick}>
          <span>{option.label}</span>
          <Icon name={option.iconName} color="black" size="normal" />
        </div>
      ))}
    </div>
  );
};
