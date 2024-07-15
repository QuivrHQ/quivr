import { BulkNotification } from "../../../types/types";
import { NotificationLoadingBar } from "../NotificationLoadingBar/NotificationLoadingBar";

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
      <NotificationLoadingBar bulkNotification={bulkNotification} />
    </div>
  );
};

export default Notification;
