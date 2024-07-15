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
      <div className={styles.loader_wrapper}>
        <div className={styles.count}>
          <span>
            {
              bulkNotification.notifications.filter(
                (notif) => notif.status !== "info"
              ).length
            }
          </span>
          <span> / </span>
          <span>{bulkNotification.notifications.length}</span>
        </div>
        <NotificationLoadingBar bulkNotification={bulkNotification} />
      </div>
    </div>
  );
};

export default Notification;
