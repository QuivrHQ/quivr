import { formatDistanceToNow } from "date-fns";
import { useRouter } from "next/navigation";

import { useBrainFetcher } from "@/app/studio/[brainId]/BrainManagementTabs/hooks/useBrainFetcher";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import styles from "./GenericNotification.module.scss";

import { BulkNotification } from "../../../types/types";

interface GenericNotificationProps {
  bulkNotification: BulkNotification;
}

export const GenericNotification = ({
  bulkNotification,
}: GenericNotificationProps): JSX.Element => {
  const { brain } = useBrainFetcher({ brainId: bulkNotification.brain_id });
  const router = useRouter();
  const { supabase } = useSupabase();
  const { updateNotifications } = useNotificationsContext();

  const navigateToBrain = () => {
    router.push(`/studio/${bulkNotification.brain_id}`); // Naviguer vers l'URL
  };

  const deleteNotification = async () => {
    await supabase
      .from("notifications")
      .delete()
      .match({ bulk_id: bulkNotification.bulk_id });

    await updateNotifications();
  };

  return (
    <div className={styles.notification} onClick={() => navigateToBrain()}>
      <div className={styles.header}>
        {brain && (
          <div className={styles.brain_name}>
            <Icon name="brain" size="small" color="dark-grey" />
            <span>{brain.name}</span>
          </div>
        )}
        <div
          onClick={(event) => {
            event.stopPropagation();
            void deleteNotification();
          }}
        >
          <Icon
            name="delete"
            size="small"
            color="dangerous"
            handleHover={true}
          />
        </div>
      </div>
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
