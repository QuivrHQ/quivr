import { formatDistanceToNow } from "date-fns";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { useBrainFetcher } from "@/app/studio/[brainId]/BrainManagementTabs/hooks/useBrainFetcher";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";
import { Brain } from "@/lib/context/BrainProvider/types";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import styles from "./FeedingNotification.module.scss";
import { NotificationLoadingBar } from "./NotificationLoadingBar/NotificationLoadingBar";

import { BulkNotification, NotificationType } from "../../../types/types";

interface FeedingNotificationProps {
  bulkNotification: BulkNotification;
}

const NotificationHeader = ({
  bulkNotification,
  brain,
  onDelete,
  allNotifsProcessed,
}: {
  bulkNotification: BulkNotification;
  brain?: Brain;
  onDelete: () => void;
  allNotifsProcessed: boolean;
}) => (
  <div className={styles.header}>
    <div className={styles.left}>
      <span className={styles.title}>
        <span>
          {bulkNotification.category === "upload" &&
            `${allNotifsProcessed ? "Uploaded" : "Uploading"} files `}
          {bulkNotification.category === "crawl" &&
            `${allNotifsProcessed ? "Crawled" : "Crawling"} websites `}
          {bulkNotification.category === "sync" &&
            `${allNotifsProcessed ? "Synced" : "Syncing"} files `}
        </span>
        for
      </span>
      {brain && (
        <div className={styles.brain_name}>
          <Icon name="brain" size="small" color="dark-grey" />
          <span>{brain.name}</span>
        </div>
      )}
    </div>
    {bulkNotification.notifications.every(
      (notif) => notif.status !== "info"
    ) && (
      <div
        onClick={(event) => {
          event.stopPropagation();
          onDelete();
        }}
      >
        <Icon name="delete" size="small" color="dangerous" handleHover={true} />
      </div>
    )}
  </div>
);

const NotificationIcon = ({
  notifications,
}: {
  notifications: NotificationType[];
}) => {
  const hasPending = notifications.some((notif) => notif.status === "info");
  const allSuccess = notifications.every((notif) => notif.status === "success");

  if (hasPending) {
    return <LoaderIcon size="small" color="primary" />;
  }
  if (allSuccess) {
    return <Icon color="success" name="check" size="small" />;
  }

  return <Icon color="warning" name="warning" size="small" />;
};

const NotificationCount = ({
  notifications,
}: {
  notifications: NotificationType[];
}) => {
  const total = notifications.length;
  const completed = notifications.filter(
    (notif) => notif.status !== "info"
  ).length;
  const hasError = notifications.some((notif) => notif.status === "error");

  let className = "";
  if (completed === total) {
    className = hasError ? styles.warning : styles.success;
  }

  return (
    <div className={`${styles.count} ${className}`}>
      {`${completed} / ${total}`}
    </div>
  );
};

export const FeedingNotification = ({
  bulkNotification,
}: FeedingNotificationProps): JSX.Element => {
  const { brain } = useBrainFetcher({ brainId: bulkNotification.brain_id });
  const { supabase } = useSupabase();
  const { updateNotifications } = useNotificationsContext();
  const [errorsOpened, setErrorsOpened] = useState(false);
  const [successOpened, setSuccessOpened] = useState(false);
  const router = useRouter();

  const navigateToBrain = () => {
    router.push(`/studio/${bulkNotification.brain_id}`);
  };

  const allNotifsProcessed = bulkNotification.notifications.every(
    (notif) => notif.status !== "info"
  );

  const deleteNotification = async () => {
    await supabase
      .from("notifications")
      .delete()
      .match({ bulk_id: bulkNotification.bulk_id });

    await updateNotifications();
  };

  return (
    <div className={styles.notification} onClick={() => navigateToBrain()}>
      <NotificationHeader
        bulkNotification={bulkNotification}
        brain={brain}
        onDelete={() => void deleteNotification()}
        allNotifsProcessed={allNotifsProcessed}
      />
      {bulkNotification.notifications.some(
        (notif) => notif.status === "info"
      ) ? (
        <div className={styles.loader_wrapper}>
          <div className={styles.left}>
            <div className={styles.icon_info}>
              <NotificationIcon
                notifications={bulkNotification.notifications}
              />
            </div>
            <NotificationCount notifications={bulkNotification.notifications} />
          </div>
          <NotificationLoadingBar bulkNotification={bulkNotification} />
        </div>
      ) : (
        <div className={styles.status_report}>
          {bulkNotification.notifications.some(
            (notif) => notif.status === "success"
          ) && (
            <div
              className={styles.success}
              onClick={(event) => {
                event.stopPropagation();
                setSuccessOpened(!successOpened);
                setErrorsOpened(false);
              }}
            >
              <Icon name="check" size="small" color="success" />
              <span>
                {
                  bulkNotification.notifications.filter(
                    (notif) => notif.status === "success"
                  ).length
                }
              </span>
            </div>
          )}
          {bulkNotification.notifications.some(
            (notif) => notif.status === "error"
          ) && (
            <div
              className={styles.error}
              onClick={(event) => {
                event.stopPropagation();
                setErrorsOpened(!errorsOpened);
                setSuccessOpened(false);
              }}
            >
              <Icon name="warning" size="small" color="dangerous" />
              <span>
                {
                  bulkNotification.notifications.filter(
                    (notif) => notif.status === "error"
                  ).length
                }
              </span>
            </div>
          )}
        </div>
      )}
      {errorsOpened && (
        <div className={styles.file_list}>
          {bulkNotification.notifications
            .filter((notif) => notif.status === "error")
            .map((notif, index) => (
              <Tooltip tooltip={notif.description} key={index} type="dangerous">
                <span className={`${styles.title} ${styles.error}`}>
                  {notif.title}
                </span>
              </Tooltip>
            ))}
        </div>
      )}
      {successOpened && (
        <div className={styles.file_list}>
          {bulkNotification.notifications
            .filter((notif) => notif.status === "success")
            .map((notif, index) => (
              <Tooltip tooltip={notif.description} key={index} type="success">
                <span className={`${styles.title} ${styles.success}`}>
                  {notif.title}
                </span>
              </Tooltip>
            ))}
        </div>
      )}
      <div className={styles.date_time}>
        {formatDistanceToNow(new Date(bulkNotification.datetime), {
          addSuffix: true,
        }).replace("about ", "")}
      </div>
    </div>
  );
};

export default FeedingNotification;
