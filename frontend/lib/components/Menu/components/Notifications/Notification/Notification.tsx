import { BulkNotification } from "../../../types/types";

interface NotificationProps {
  bulkNotification: BulkNotification;
  lastNotification?: boolean;
  updateNotifications: () => Promise<void>;
}

export const Notification = ({
  bulkNotification,
}: NotificationProps): JSX.Element => {
  return (
    <div>
      {
        bulkNotification.notifications.filter(
          (notif) => notif.status === "success"
        ).length
      }
      / {bulkNotification.notifications.length}
    </div>
  );
};

export default Notification;
