import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";

import styles from "./NotificationsButton.module.scss";

export const NotificationsButton = (): JSX.Element => {
  const { isVisible, setIsVisible, unreadNotifications } =
    useNotificationsContext();

  return (
    <div className={styles.button_wrapper}>
      <MenuButton
        label="Notifications"
        iconName="notifications"
        type="open"
        color="primary"
        onClick={() => setIsVisible(!isVisible)}
      />
      {!!unreadNotifications && (
        <span className={styles.badge}>
          {unreadNotifications > 9 ? "9+" : unreadNotifications}
        </span>
      )}
    </div>
  );
};
