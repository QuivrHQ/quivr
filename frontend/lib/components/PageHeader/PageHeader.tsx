import styles from "./PageHeader.module.scss";

import { Icon } from "../ui/Icon/Icon";

type Button = {
  label: string;
  color: string;
  onClick: () => void;
};

type Props = {
  iconName: string;
  label: string;
  buttons: Button[];
};

export const PageHeader = ({
  iconName,
  label,
  buttons,
}: Props): JSX.Element => {
  return (
    <div className={styles.page_header_wrapper}>
      <div className={styles.left}>
        <Icon name={iconName} size="large" color="primary" />
        <span>{label}</span>
      </div>
      {buttons.map((button, index) => (
        <button
          key={index}
          style={{ color: button.color }}
          onClick={button.onClick}
        >
          {button.label}
        </button>
      ))}
    </div>
  );
};

export default PageHeader;
