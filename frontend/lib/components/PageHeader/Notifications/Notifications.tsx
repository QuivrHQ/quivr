import { useEffect, useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { Notification } from "./Notification/Notification";
import styles from "./Notifications.module.scss";
import { NotificationType } from "./types/types";

import { Icon } from "../../ui/Icon/Icon";

export const Notifications = (): JSX.Element => {
  const [notifications, setNotifications] = useState<NotificationType[]>([]);
  const [unreadNotifications, setUnreadNotifications] = useState<number>(0);
  const [panelOpened, setPanelOpened] = useState<boolean>(false);
  const { supabase } = useSupabase();

  const updateNotifications = async () => {
    try {
      let notifs = (await supabase.from("notifications").select()).data;
      if (notifs) {
        notifs = notifs.sort(
          (a: NotificationType, b: NotificationType) =>
            new Date(b.datetime).getTime() - new Date(a.datetime).getTime()
        );
      }
      setNotifications(notifs ?? []);
      setUnreadNotifications(
        notifs?.filter((n: NotificationType) => !n.read).length ?? 0
      );
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    void (async () => {
      await updateNotifications();
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
        <span className={styles.badge}>{unreadNotifications}</span>
      </div>
      {panelOpened && (
        <div className={styles.notifications_panel}>
          {notifications.map((notification, i) => (
            <Notification
              key={i}
              notification={notification}
              lastNotification={i === notifications.length - 1}
              updateNotifications={updateNotifications}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Notifications;
