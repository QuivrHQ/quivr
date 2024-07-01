import Image from "next/image";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

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
  const { isDarkMode } = useUserSettingsContext();
  const removeCurrentBrain = (): void => {
    setCurrentBrainId(null);
  };

  if (!remainingCredits) {
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
            <Image
              className={isDarkMode ? styles.dark_image : ""}
              src={
                currentBrain.integration_logo_url
                  ? currentBrain.integration_logo_url
                  : "/default_brain_image.png"
              }
              alt="logo_image"
              width={18}
              height={18}
            />
            <span className={styles.brain_name}>{currentBrain.name}</span>
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
