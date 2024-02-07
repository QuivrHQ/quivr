import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./CurrentBrain.module.scss";

import { Icon } from "../ui/Icon/Icon";

interface CurrentBrainProps {
  allowingRemoveBrain: boolean;
}

export const CurrentBrain = ({
  allowingRemoveBrain,
}: CurrentBrainProps): JSX.Element => {
  const { currentBrain, setCurrentBrainId } = useBrainContext();

  const removeCurrentBrain = (): void => {
    setCurrentBrainId(null);
  };

  if (!currentBrain) {
    return <></>;
  }

  return (
    <div className={styles.current_brain_wrapper}>
      <div className={styles.brain_infos}>
        <div className={styles.left}>
          <span>Talking to</span>
          <div className={styles.brain_name_wrapper}>
            <Icon size="small" name="brain" color="primary" />
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
