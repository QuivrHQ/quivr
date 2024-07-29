import { useEffect, useState } from "react";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { TextButton } from "@/lib/components/ui/TextButton/TextButton";
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
  const [genericNotificationsDisplayed, setGenericNotificationsDisplayed] =
    useState<boolean>(true);
  const [feedingNotificationsDisplayed, setFeedingNotificationsDisplayed] =
    useState<boolean>(true);

  const deleteAllNotifications = async (
    notificationType: "generic" | "feeding"
  ) => {
    if (notificationType === "generic") {
      await supabase.from("notifications").delete().match({
        category: "generic",
      });
    } else {
      await supabase
        .from("notifications")
        .delete()
        .not("category", "eq", "generic");
    }

    await updateNotifications();
  };

  const handleClickOutside = (event: MouseEvent) => {
    const target = event.target as Node;
    const panel = document.getElementById("notifications-panel");
    const button = document.getElementById("notifications-button");

    if (!panel || !button) {
      return;
    }

    if (!panel.contains(target) && !button.contains(target)) {
      setIsVisible(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const hasGenericNotifications = () => {
    return bulkNotifications.some((notif) => notif.category === "generic");
  };

  const renderGenericNotifications = () => {
    return (
      <>
        {bulkNotifications.map((notification, i) =>
          notification.category === "generic" ? (
            <GenericNotification key={i} bulkNotification={notification} />
          ) : null
        )}
      </>
    );
  };

  const renderFeedingNotifications = () => {
    return (
      <>
        <div
          className={styles.notifications_panel_header}
          onClick={() =>
            setFeedingNotificationsDisplayed(!feedingNotificationsDisplayed)
          }
        >
          <div className={styles.left}>
            {isMobile && !hasGenericNotifications() && (
              <Icon
                name="hide"
                size="small"
                handleHover={true}
                color="black"
                onClick={() => setIsVisible(false)}
              />
            )}
            <span className={styles.title}>Knowledge feeding in progress</span>
            <div className={styles.icon}>
              <Icon
                name={
                  feedingNotificationsDisplayed ? "chevronRight" : "chevronDown"
                }
                size="normal"
                color="black"
              />
            </div>
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

        {feedingNotificationsDisplayed &&
          bulkNotifications.map((notification, i) =>
            notification.category !== "generic" ? (
              <FeedingNotification key={i} bulkNotification={notification} />
            ) : null
          )}
      </>
    );
  };

  return (
    <div id="notifications-panel" className={styles.notifications_wrapper}>
      <div className={styles.notifications_panel}>
        {(bulkNotifications.length === 0 || hasGenericNotifications()) && (
          <div
            className={styles.notifications_panel_header}
            onClick={() =>
              setGenericNotificationsDisplayed(!genericNotificationsDisplayed)
            }
          >
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
              <div className={styles.icon}>
                <Icon
                  name={
                    genericNotificationsDisplayed
                      ? "chevronRight"
                      : "chevronDown"
                  }
                  size="normal"
                  color="black"
                />
              </div>
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
        )}

        {bulkNotifications.length === 0 && (
          <div className={styles.no_notifications}>
            You have no notifications
          </div>
        )}

        {hasGenericNotifications() &&
          genericNotificationsDisplayed &&
          renderGenericNotifications()}

        {bulkNotifications.some((notif) => notif.category !== "generic") &&
          renderFeedingNotifications()}
      </div>
    </div>
  );
};

export default Notifications;
