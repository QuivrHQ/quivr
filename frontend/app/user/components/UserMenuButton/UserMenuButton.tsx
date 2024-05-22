import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./UserMenuButton.module.scss";

interface UserMenuButtonProps {
  label: string;
  last?: boolean;
  iconName: string;
  onClick: () => void;
  selected?: boolean;
}

export const UserMenuButton = ({
  label,
  last,
  iconName,
  onClick,
  selected,
}: UserMenuButtonProps): JSX.Element => {
  return (
    <div
      className={`${styles.menu_button} ${last ? styles.last : ""} ${
        selected ? styles.selected : ""
      }`}
      onClick={() => onClick()}
    >
      <Icon name={iconName} size="small" color="black" />
      <span className={styles.label}>{label}</span>
    </div>
  );
};
