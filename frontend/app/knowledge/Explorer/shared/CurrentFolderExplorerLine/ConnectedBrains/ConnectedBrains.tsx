import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";
import { Brain } from "@/lib/context/BrainProvider/types";

import styles from "./ConnectedBrains.module.scss";

interface ConnectedbrainsProps {
  connectedBrains: Brain[];
}

const ConnectedBrains = ({
  connectedBrains,
}: ConnectedbrainsProps): JSX.Element => {
  return (
    <div className={styles.main_container}>
      {connectedBrains.map((brain) => (
        <Tooltip key={brain.id} tooltip={brain.name}>
          <div className={styles.brain_container}>
            <div
              className={styles.sample_wrapper}
              style={{ backgroundColor: brain.snippet_color }}
            >
              <span>{brain.snippet_emoji}</span>
            </div>
          </div>
        </Tooltip>
      ))}
    </div>
  );
};

export default ConnectedBrains;
