import styles from "./UserMenuCard.module.scss";

import { UserMenuCardProps } from "../types/types";

export const UserMenuCard = ({
  title,
  subtitle,
}: UserMenuCardProps): JSX.Element => {
  return (
    <div className={styles.menu_card_container}>
      <h1>{title}</h1>
      <h2>{subtitle}</h2>
    </div>
  );
};
