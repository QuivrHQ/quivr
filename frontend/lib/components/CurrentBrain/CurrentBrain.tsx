import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";

import styles from "./CurrentBrain.module.scss";

import { Icon } from "../ui/Icon/Icon";

interface CurrentBrainProps {
  allowingRemoveBrain: boolean;
  remainingCredits: number | null;
}

export const CurrentBrain = ({
  allowingRemoveBrain,
  remainingCredits,
}: CurrentBrainProps): JSX.Element => {
  const { currentBrain, setCurrentBrainId } = useBrainContext();
  const removeCurrentBrain = (): void => {
    setCurrentBrainId(null);
  };
  const { bulkNotifications } = useNotificationsContext();

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
    return (
      <div className={styles.no_brain_selected}>
        <span>
          Press <strong className={styles.strong}>@</strong> to select a Brain
        </span>
      </div>
    );
  }

  return (
    <div className={styles.current_brain_wrapper}>
      <div className={styles.brain_infos}>
        <div className={styles.left}>
          <span className={styles.title}>Talking to</span>
          <div className={styles.brain_name_wrapper}>
            <Icon name="brain" size="small" color="black" />
            <span className={styles.brain_name}>{currentBrain.name}</span>
            {bulkNotifications.some(
              (bulkNotif) =>
                bulkNotif.brain_id === currentBrain.id &&
                bulkNotif.notifications.some((notif) => notif.status === "info")
            ) && (
              <div className={styles.warning}>
                <Icon name="warning" color="warning" size="small"></Icon>
                <span>Processing knowledges</span>
              </div>
            )}
          </div>
        </div>
        {allowingRemoveBrain && (
          <div
            onClick={(event) => {
              event.nativeEvent.stopImmediatePropagation();
              removeCurrentBrain();
            }}
          >
            <Icon size="normal" name="close" color="black" handleHover={true} />
          </div>
        )}
      </div>
    </div>
  );
};
