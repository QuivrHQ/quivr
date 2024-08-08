import Image from "next/image";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";

import styles from "./CurrentBrain.module.scss";

import { Icon } from "../ui/Icon/Icon";
import { LoaderIcon } from "../ui/LoaderIcon/LoaderIcon";

interface CurrentBrainProps {
  allowingRemoveBrain: boolean;
  remainingCredits: number | null;
  isNewBrain?: boolean;
}

const BrainNameAndImage = ({
  currentBrain,
  isNewBrain,
}: {
  currentBrain: MinimalBrainForUser;
  isNewBrain: boolean;
}) => {
  return (
    <>
      {currentBrain.image_url ? (
        <Image src={currentBrain.image_url} alt="" width={18} height={18} />
      ) : (
        <Icon name="brain" size="normal" color="black" />
      )}
      <span className={`${styles.brain_name} ${isNewBrain ? styles.new : ""}`}>
        {currentBrain.display_name ?? currentBrain.name}
      </span>
    </>
  );
};

const ProcessingNotification = ({
  currentBrain,
  bulkNotifications,
}: {
  currentBrain?: MinimalBrainForUser;
  bulkNotifications: Array<{
    brain_id: string;
    notifications: Array<{ status: string }>;
  }>;
}) => {
  const isProcessing =
    currentBrain &&
    bulkNotifications.some(
      (bulkNotif) =>
        bulkNotif.brain_id === currentBrain.id &&
        bulkNotif.notifications.some((notif) => notif.status === "info")
    );

  return (
    isProcessing && (
      <div className={styles.warning}>
        <LoaderIcon size="small" color="warning" />
        <span>Processing knowledges</span>
      </div>
    )
  );
};

export const CurrentBrain = ({
  allowingRemoveBrain,
  remainingCredits,
  isNewBrain,
}: CurrentBrainProps): JSX.Element => {
  const { currentBrain, setCurrentBrainId } = useBrainContext();
  const { bulkNotifications } = useNotificationsContext();

  const removeCurrentBrain = (): void => {
    setCurrentBrainId(null);
  };

  if (remainingCredits === 0) {
    return (
      <div className={styles.no_credits_left}>
        <span>
          You’ve run out of credits! Upgrade your plan now to continue chatting.
        </span>
      </div>
    );
  }

  if (!currentBrain) {
    return <></>;
  }

  return (
    <div className={styles.current_brain_wrapper}>
      <div className={styles.brain_infos}>
        <div className={styles.left}>
          <span className={styles.title}>Talking to</span>
          <div className={styles.brain_name_wrapper}>
            <BrainNameAndImage
              currentBrain={currentBrain}
              isNewBrain={!!isNewBrain}
            />
            <ProcessingNotification
              currentBrain={currentBrain}
              bulkNotifications={bulkNotifications}
            />
          </div>
        </div>
        {allowingRemoveBrain && (
          <div
            onClick={(event) => {
              event.nativeEvent.stopImmediatePropagation();
              removeCurrentBrain();
            }}
          >
            <Icon size="normal" name="close" color="black" handleHover />
          </div>
        )}
      </div>
    </div>
  );
};
