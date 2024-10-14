import { UUID } from "crypto";
import { useRouter } from "next/navigation";

import { KnowledgeStatus } from "@/lib/api/sync/types";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";
import { Brain } from "@/lib/context/BrainProvider/types";

import styles from "./ConnectedBrains.module.scss";

interface ConnectedbrainsProps {
  connectedBrains: Brain[];
  knowledgeStatus?: KnowledgeStatus;
}

const ConnectedBrains = ({
  connectedBrains,
  knowledgeStatus,
}: ConnectedbrainsProps): JSX.Element => {
  const router = useRouter();

  const navigateToBrain = (brainId: UUID) => {
    router.push(`/studio/${brainId}`);
  };

  const isKnowledgeStatusWaiting = (status?: KnowledgeStatus): boolean => {
    return status === "RESERVED" || status === "PROCESSING";
  };

  return (
    <div className={styles.main_container}>
      {connectedBrains.map((brain) => (
        <Tooltip key={brain.id} tooltip={brain.name}>
          <>
            <div
              className={`${styles.brain_container} ${
                isKnowledgeStatusWaiting(knowledgeStatus) ? styles.waiting : ""
              }`}
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
            {isKnowledgeStatusWaiting(knowledgeStatus) && (
              <div className={styles.waiting_icon}>
                <Icon color="black" name="waiting" size="small" />
              </div>
            )}
          </>
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
