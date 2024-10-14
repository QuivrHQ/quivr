import { UUID } from "crypto";
import { useRouter } from "next/navigation";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";
import { Brain } from "@/lib/context/BrainProvider/types";

import styles from "./ConnectedBrains.module.scss";

interface ConnectedbrainsProps {
  connectedBrains: Brain[];
}

const ConnectedBrains = ({
  connectedBrains,
}: ConnectedbrainsProps): JSX.Element => {
  const router = useRouter();

  const navigateToBrain = (brainId: UUID) => {
    router.push(`/studio/${brainId}`);
  };

  return (
    <div className={styles.main_container}>
      {connectedBrains.map((brain) => (
        <Tooltip key={brain.id} tooltip={brain.name}>
          <div
            className={styles.brain_container}
            onClick={() => {
              navigateToBrain(brain.brain_id ?? brain.id);
            }}
          >
            <div
              className={styles.sample_wrapper}
              style={{ backgroundColor: brain.snippet_color }}
            >
              <span>{brain.snippet_emoji}</span>
            </div>
          </div>
        </Tooltip>
      ))}
      <Tooltip tooltip="Add to brains">
        <div>
          <Icon name="add" color="black" size="normal" handleHover={true} />
        </div>
      </Tooltip>
    </div>
  );
};

export default ConnectedBrains;
