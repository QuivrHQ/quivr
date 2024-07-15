import Icon from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

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
  return (
    <div
      className={`${styles.notification} ${
        lastNotification ? styles.last : ""
      }`}
    >
      <span></span>
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
            {`${Math.round(
              (bulkNotification.notifications.filter(
                (notif) => notif.status !== "info"
              ).length /
                bulkNotification.notifications.length) *
                100
            )}%`}
          </div>
        </div>
        <NotificationLoadingBar bulkNotification={bulkNotification} />
      </div>
    </div>
  );
};

export default Notification;
