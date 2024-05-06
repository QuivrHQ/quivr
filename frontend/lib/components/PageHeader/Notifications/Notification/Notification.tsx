import { formatDistanceToNow } from "date-fns";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./Notification.module.scss";

import { NotificationType } from "../types/types";

interface NotificationProps {
  notification: NotificationType;
  lastNotification?: boolean;
}

export const Notification = ({
  notification,
  lastNotification,
}: NotificationProps): JSX.Element => {
  return (
    <div
      className={`${styles.notification_wrapper} ${
        lastNotification ? styles.no_border : ""
      }`}
    >
      <div className={styles.header}>
        <div className={styles.left}>
          <div className={styles.badge}></div>
          <span className={styles.title}>{notification.title}</span>
        </div>
        <div className={styles.icons}>
          <Icon name="delete" color="black" handleHover={true} size="small" />
          <Icon name="delete" color="black" handleHover={true} size="small" />
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
