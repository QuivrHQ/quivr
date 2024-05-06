import { useEffect, useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { Notification } from "./Notification/Notification";
import styles from "./Notifications.module.scss";
import { NotificationType } from "./types/types";

import { Icon } from "../../ui/Icon/Icon";

export const Notifications = (): JSX.Element => {
  const [notifications, setNotifications] = useState<NotificationType[]>([]);
  const [panelOpened, setPanelOpened] = useState<boolean>(false);
  const { supabase } = useSupabase();

  useEffect(() => {
    void (async () => {
      try {
        const notifs = (await supabase.from("notifications").select()).data;
        console.info("Notifications", notifs);
        setNotifications(notifs ?? []);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  return (
    <div className={styles.notifications_wrapper}>
      <div onClick={() => setPanelOpened(!panelOpened)}>
        <Icon
          name="notifications"
          size="large"
          color="black"
          handleHover={true}
        />
        <span className={styles.badge}>{notifications.length}</span>
      </div>
      {panelOpened && (
        <div className={styles.notifications_panel}>
          {notifications.map((notification, i) => (
            <Notification
              key={i}
              notification={notification}
              lastNotification={i === notifications.length - 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Notifications;
