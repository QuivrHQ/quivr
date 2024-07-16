import { useEffect } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import TextButton from "@/lib/components/ui/TextButton/TextButton";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useDevice } from "@/lib/hooks/useDevice";

import { FeedingNotification } from "./FeedingNotification/FeedingNotification";
import { GenericNotification } from "./GenericNotification/GenericNotification";
import styles from "./Notifications.module.scss";

export const Notifications = (): JSX.Element => {
  const { bulkNotifications, updateNotifications, setIsVisible } =
    useNotificationsContext();
  const { isMobile } = useDevice();
  const { supabase } = useSupabase();

  const deleteAllNotifications = async (
    notificationType: "generic" | "feeding"
  ) => {
    for (const notifications of bulkNotifications) {
      for (const notification of notifications.notifications) {
        if (
          notificationType === "generic" &&
          notification.category === "generic"
        ) {
          await supabase
            .from("notifications")
            .delete()
            .eq("id", notification.id);
        } else if (
          notificationType === "feeding" &&
          notification.category !== "generic"
        ) {
          await supabase
            .from("notifications")
            .delete()
            .eq("id", notification.id);
        }
      }
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
        {bulkNotifications.length === 0 ||
        bulkNotifications.some((notif) => notif.category === "generic") ? (
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
                label="Delete all"
                color="black"
                onClick={() => void deleteAllNotifications("generic")}
                small={true}
              />
            </div>
          </div>
        ) : null}
        {bulkNotifications.length === 0 && (
          <div className={styles.no_notifications}>
            You have no notifications
          </div>
        )}
        {bulkNotifications.some((notif) => notif.category === "generic") && (
          <>
            {bulkNotifications.map((notification, i) =>
              notification.category === "generic" ? (
                <GenericNotification key={i} bulkNotification={notification} />
              ) : null
            )}
          </>
        )}
        {bulkNotifications.some((notif) => notif.category !== "generic") && (
          <>
            <div className={styles.notifications_panel_header}>
              <div className={styles.left}>
                {isMobile &&
                  !bulkNotifications.some(
                    (notif) => notif.category === "generic"
                  ) && (
                    <Icon
                      name="hide"
                      size="small"
                      handleHover={true}
                      color="black"
                      onClick={() => setIsVisible(false)}
                    />
                  )}
                <span className={styles.title}>
                  Knowledge feeding in progress
                </span>
              </div>
              <div className={styles.buttons}>
                <TextButton
                  label="Delete all"
                  color="black"
                  onClick={() => void deleteAllNotifications("feeding")}
                  small={true}
                />
              </div>
            </div>

            {bulkNotifications.map((notification, i) =>
              notification.category !== "generic" ? (
                <FeedingNotification key={i} bulkNotification={notification} />
              ) : null
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Notifications;
