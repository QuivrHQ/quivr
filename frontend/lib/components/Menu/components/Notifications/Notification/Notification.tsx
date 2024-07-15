import { useBrainFetcher } from "@/app/studio/[brainId]/BrainManagementTabs/hooks/useBrainFetcher";
import Icon from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import styles from "./Notification.module.scss";

import { BulkNotification } from "../../../types/types";
import { NotificationLoadingBar } from "../NotificationLoadingBar/NotificationLoadingBar";

interface NotificationProps {
  bulkNotification: BulkNotification;
  lastNotification?: boolean;
  updateNotifications: () => Promise<void>;
}

export const Notification = ({
  bulkNotification,
  lastNotification,
}: NotificationProps): JSX.Element => {
  const { brain } = useBrainFetcher({ brainId: bulkNotification.brain_id });
  const { supabase } = useSupabase();
  const { updateNotifications } = useNotificationsContext();

  const deleteNotification = async () => {
    for (const notification of bulkNotification.notifications) {
      await supabase.from("notifications").delete().eq("id", notification.id);
    }
    await updateNotifications();
  };

  return (
    <div
      className={`${styles.notification} ${
        lastNotification ? styles.last : ""
      }`}
    >
      <div className={styles.header}>
        <div className={styles.left}>
          <span className={styles.title}>
            {bulkNotification.category === "upload" && "Uploading files "}
            {bulkNotification.category === "crawl" && "Crawling websites "}
            {bulkNotification.category === "sync" && "Syncing files "}
            for
          </span>
          {brain && (
            <div className={styles.brain_name}>
              <Icon name="brain" size="small" color="dark-grey" />
              <span>{brain.name}</span>
            </div>
          )}
        </div>
        <Icon
          name="delete"
          size="small"
          color="dangerous"
          handleHover={true}
          onClick={deleteNotification}
        />
      </div>
      <div className={styles.loader_wrapper}>
        <div className={styles.left}>
          <div className={styles.icon_info}>
            {bulkNotification.notifications.some(
              (notif) => notif.status === "info"
            ) ? (
              <LoaderIcon size="small" color="primary" />
            ) : bulkNotification.notifications.every(
                (notif) => notif.status === "success"
              ) ? (
              <Icon color="success" name="check" size="small" />
            ) : (
              <Icon color="warning" name="warning" size="small" />
            )}
          </div>

          <div
            className={`${styles.count} ${
              bulkNotification.notifications.every(
                (notif) => notif.status !== "info"
              )
                ? bulkNotification.notifications.some(
                    (notif) => notif.status === "error"
                  )
                  ? styles.warning
                  : styles.success
                : ""
            }`}
          >
            {`${
              bulkNotification.notifications.filter(
                (notif) => notif.status !== "info"
              ).length
            } / ${bulkNotification.notifications.length}`}
          </div>
        </div>
        <NotificationLoadingBar bulkNotification={bulkNotification} />
      </div>
    </div>
  );
};

export default Notification;
