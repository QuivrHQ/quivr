import { useEffect } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import TextButton from "@/lib/components/ui/TextButton/TextButton";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useDevice } from "@/lib/hooks/useDevice";

import { Notification } from "./Notification/Notification";
import styles from "./Notifications.module.scss";

export const Notifications = (): JSX.Element => {
  const {
    notifications,
    updateNotifications,
    unreadNotifications,
    setIsVisible,
  } = useNotificationsContext();
  const { supabase } = useSupabase();
  const { isMobile } = useDevice();

  const deleteAllNotifications = async () => {
    for (const notification of notifications) {
      await supabase.from("notifications").delete().eq("id", notification.id);
    }
    await updateNotifications();
  };

  const markAllAsRead = async () => {
    for (const notification of notifications) {
      await supabase
        .from("notifications")
        .update({ read: true })
        .eq("id", notification.id);
    }
    await updateNotifications();
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Node;
      const panel = document.getElementById("notifications-panel");
      const button = document.getElementById("notifications-button");

      if (!panel?.contains(target) && !button?.contains(target)) {
        setIsVisible(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div id="notifications-panel" className={styles.notifications_wrapper}>
      <div className={styles.notifications_panel}>
        <div className={styles.notifications_panel_header}>
          <div className={styles.left}>
            {isMobile && (
              <Icon
                name="hide"
                size="small"
                handleHover={true}
                color="black"
                onClick={() => setIsVisible(false)}
              />
            )}
            <span className={styles.title}>Notifications</span>
          </div>
          <div className={styles.buttons}>
            <TextButton
              label="Mark all as read"
              color="black"
              onClick={() => void markAllAsRead()}
              disabled={unreadNotifications === 0}
              small={true}
            />
            <span>|</span>
            <TextButton
              label="Delete all"
              color="black"
              onClick={() => void deleteAllNotifications()}
              disabled={notifications.length === 0}
              small={true}
            />
          </div>
        </div>
        {notifications.length === 0 && (
          <div className={styles.no_notifications}>
            You have no notifications
          </div>
        )}
        {notifications.map((notification, i) => (
          <Notification
            key={i}
            notification={notification}
            lastNotification={i === notifications.length - 1}
            updateNotifications={updateNotifications}
          />
        ))}
      </div>
    </div>
  );
};

export default Notifications;
