import { BulkNotification } from "@/lib/components/Menu/types/types";

import styles from "./NotificationLoadingBar.module.scss";

interface NotificationProps {
  bulkNotification: BulkNotification;
}

interface StatusCounts {
  [status: string]: number;
}

export const NotificationLoadingBar = ({
  bulkNotification,
}: NotificationProps): JSX.Element => {
  const statusCounts = bulkNotification.notifications.reduce(
    (acc: StatusCounts, notification) => {
      const { status } = notification;
      acc[status] = (acc[status] ?? 0) + 1;

      return acc;
    },
    {} as StatusCounts
  );

  const totalCount = bulkNotification.notifications.length;

  const statusOrder = ["success", "error", "warning", "info"];
  const sortedStatusCounts = Object.entries(statusCounts).sort(
    (a, b) => statusOrder.indexOf(a[0]) - statusOrder.indexOf(b[0])
  );

  return (
    <div className={styles.loading_bar}>
      {sortedStatusCounts.map(([status, count]) => (
        <div
          key={status}
          className={`${styles.bar_section} ${styles[status]}`}
          style={{
            width: `${(Number(count) / totalCount) * 100}%`,
          }}
        />
      ))}
    </div>
  );
};

export default NotificationLoadingBar;
