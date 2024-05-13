import { formatDistanceToNow } from "date-fns";

import Icon from "@/lib/components/ui/Icon/Icon";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import styles from "./Notification.module.scss";

import { NotificationType } from "../types/types";

interface NotificationProps {
  notification: NotificationType;
  lastNotification?: boolean;
  updateNotifications: () => Promise<void>;
}

export const Notification = ({
  notification,
  lastNotification,
  updateNotifications,
}: NotificationProps): JSX.Element => {
  const { supabase } = useSupabase();

  const deleteNotif = async () => {
    await supabase.from("notifications").delete().eq("id", notification.id);
    await updateNotifications();
  };

  const readNotif = async () => {
    await supabase
      .from("notifications")
      .update({ read: !notification.read })
      .eq("id", notification.id);

    await updateNotifications();
  };

  return (
    <div
      className={`${styles.notification_wrapper} ${
        lastNotification ? styles.no_border : ""
      } ${notification.read ? styles.read : ""}`}
    >
      <div className={styles.header}>
        <div className={styles.left}>
          {!notification.read && <div className={styles.badge}></div>}
          <span className={styles.title}>{notification.title}</span>
        </div>
        <div className={styles.icons}>
          <Icon
            name={notification.read ? "unread" : "read"}
            color="black"
            handleHover={true}
            size="normal"
            onClick={() => readNotif()}
          />
          <Icon
            name="delete"
            color="black"
            handleHover={true}
            size="normal"
            onClick={() => deleteNotif()}
          />
        </div>
      </div>
      <span className={`${styles.description} ${styles[notification.status]} `}>
        {notification.description}
      </span>
      <span className={styles.date}>
        {formatDistanceToNow(new Date(notification.datetime), {
          addSuffix: true,
        }).replace("about ", "")}
      </span>
    </div>
  );
};

export default Notification;
