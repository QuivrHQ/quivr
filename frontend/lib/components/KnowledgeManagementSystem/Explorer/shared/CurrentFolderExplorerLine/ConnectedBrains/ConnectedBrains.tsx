import { UUID } from "crypto";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { KMSElement, KnowledgeStatus } from "@/lib/api/sync/types";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";
import { Brain } from "@/lib/context/BrainProvider/types";

import AddToBrainsModal from "./AddToBrainsModal/AddToBrainsModal";
import styles from "./ConnectedBrains.module.scss";

interface ConnectedbrainsProps {
  connectedBrains: Brain[];
  knowledge?: KMSElement;
}

interface RemainingBrainsTooltipProps {
  remainingBrains: Brain[];
  navigateToBrain: (brainId: UUID) => void;
  isKnowledgeStatusWaiting: (status?: KnowledgeStatus) => boolean;
  knowledgeStatus?: KnowledgeStatus;
}

const RemainingBrainsTooltip = ({
  remainingBrains,
  navigateToBrain,
  isKnowledgeStatusWaiting,
  knowledgeStatus,
}: RemainingBrainsTooltipProps): JSX.Element => {
  return (
    <div className={styles.remaining_brains_tooltip}>
      {remainingBrains.map((brain) => (
        <Tooltip key={brain.id} tooltip={brain.name}>
          <div
            className={styles.brain_container}
            onClick={() => {
              navigateToBrain(brain.brain_id ?? brain.id);
            }}
          >
            <div
              className={`${styles.sample_wrapper} ${
                isKnowledgeStatusWaiting(knowledgeStatus) ||
                knowledgeStatus === "ERROR"
                  ? styles.waiting
                  : ""
              }`}
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

const ConnectedBrains = ({
  connectedBrains,
  knowledge,
}: ConnectedbrainsProps): JSX.Element => {
  const [showAddToBrainModal, setShowAddToBrainModal] =
    useState<boolean>(false);
  const [showRemainingBrains, setShowRemainingBrains] =
    useState<boolean>(false);
  const router = useRouter();

  const navigateToBrain = (brainId: UUID) => {
    router.push(`/studio/${brainId}`);
  };

  const isKnowledgeStatusWaiting = (status?: KnowledgeStatus): boolean => {
    return status === "RESERVED" || status === "PROCESSING";
  };

  const handleAddClick = (event: React.MouseEvent) => {
    event.stopPropagation();
    event.preventDefault();
    setShowAddToBrainModal(true);
  };

  const handleModalClose = () => {
    setShowAddToBrainModal(false);
  };

  const brainsToShow = connectedBrains.slice(0, 5);
  const remainingBrains = connectedBrains.slice(5);
  const showMore = connectedBrains.length > 5;

  return (
    <>
      <div className={styles.main_container}>
        {brainsToShow.map((brain) => (
          <Tooltip key={brain.id} tooltip={brain.name}>
            <>
              <div
                className={styles.brain_container}
                onClick={() => {
                  navigateToBrain(brain.brain_id ?? brain.id);
                }}
              >
                <div
                  className={`${styles.sample_wrapper} ${
                    isKnowledgeStatusWaiting(knowledge?.status) ||
                    knowledge?.status === "ERROR"
                      ? styles.waiting
                      : ""
                  }`}
                  style={{ backgroundColor: brain.snippet_color }}
                >
                  <span>{brain.snippet_emoji}</span>
                </div>
                {isKnowledgeStatusWaiting(knowledge?.status) && (
                  <div className={styles.waiting_icon}>
                    <LoaderIcon color="black" size="small" />
                  </div>
                )}
                {knowledge?.status === "ERROR" && (
                  <div className={styles.waiting_icon}>
                    <Icon name="warning" color="black" size="small" />
                  </div>
                )}
              </div>
            </>
          </Tooltip>
        ))}
        {showMore && (
          <>
            {showRemainingBrains && (
              <div className={styles.remaining_brains_container}>
                <RemainingBrainsTooltip
                  remainingBrains={remainingBrains}
                  navigateToBrain={navigateToBrain}
                  isKnowledgeStatusWaiting={isKnowledgeStatusWaiting}
                  knowledgeStatus={knowledge?.status}
                />
              </div>
            )}
            <div
              className={styles.more_brains}
              onClick={() => setShowRemainingBrains(!showRemainingBrains)}
            >
              ...
            </div>
          </>
        )}
        <Tooltip tooltip="Add to brains" delayDuration={250}>
          <div onClick={handleAddClick}>
            <Icon name="add" color="black" size="normal" handleHover={true} />
          </div>
        </Tooltip>
      </div>
      {showAddToBrainModal && (
        <div
          className={styles.modal_content}
          onClick={(e) => e.stopPropagation()}
        >
          <AddToBrainsModal
            isOpen={showAddToBrainModal}
            setIsOpen={handleModalClose}
            knowledge={knowledge}
          />
        </div>
      )}
    </>
  );
};

export default ConnectedBrains;
