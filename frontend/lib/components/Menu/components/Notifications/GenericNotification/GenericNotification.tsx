import { formatDistanceToNow } from "date-fns";

import { useBrainFetcher } from "@/app/studio/[brainId]/BrainManagementTabs/hooks/useBrainFetcher";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./GenericNotification.module.scss";

import { BulkNotification } from "../../../types/types";

interface GenericNotificationProps {
  bulkNotification: BulkNotification;
}

export const GenericNotification = ({
  bulkNotification,
}: GenericNotificationProps): JSX.Element => {
  const { brain } = useBrainFetcher({ brainId: bulkNotification.brain_id });

  return (
    <div className={styles.notification}>
      {brain && (
        <div className={styles.brain_name}>
          <Icon name="brain" size="small" color="dark-grey" />
          <span>{brain.name}</span>
        </div>
      )}
      <span className={styles.content}>
        {bulkNotification.notifications[0].description}
      </span>
      <div className={styles.date_time}>
        {formatDistanceToNow(new Date(bulkNotification.datetime), {
          addSuffix: true,
        }).replace("about ", "")}
      </div>
    </div>
  );
};

export default GenericNotification;
