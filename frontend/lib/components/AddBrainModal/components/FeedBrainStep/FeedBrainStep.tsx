import { useEffect, useState } from "react";

import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { OpenedConnection } from "@/lib/api/sync/types";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { createHandleGetButtonProps } from "@/lib/helpers/handleConnectionButtons";
import { useUserData } from "@/lib/hooks/useUserData";

import styles from "./FeedBrainStep.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const FeedBrainStep = (): JSX.Element => {
  const { currentStepIndex, goToPreviousStep, goToNextStep } =
    useBrainCreationSteps();
  const { userIdentityData } = useUserData();
  const {
    currentSyncId,
    setCurrentSyncId,
    openedConnections,
    setOpenedConnections,
  } = useFromConnectionsContext();
  const [currentConnection, setCurrentConnection] = useState<
    OpenedConnection | undefined
  >(undefined);
  const { knowledgeToFeed } = useKnowledgeToFeedContext();

  useEffect(() => {
    setCurrentConnection(
      openedConnections.find(
        (connection) => connection.user_sync_id === currentSyncId
      )
    );
  }, [currentSyncId]);

  const getButtonProps = createHandleGetButtonProps(
    currentConnection,
    openedConnections,
    setOpenedConnections,
    currentSyncId,
    setCurrentSyncId
  );

  const renderFeedBrain = () => (
    <>
      {!userIdentityData?.onboarded && (
        <div className={styles.tutorial}>
          <MessageInfoBox type="tutorial">
            <span>
              Upload documents or add URLs to add knowledges to your brain.
            </span>
          </MessageInfoBox>
        </div>
      )}
      <div className={styles.feed_brain}>
        <span className={styles.title}>Feed your brain</span>
        <KnowledgeToFeed hideBrainSelector={true} />
      </div>
    </>
  );

  const renderButtons = () => {
    const buttonProps = getButtonProps();

    return (
      <div className={styles.buttons_wrapper}>
        {currentSyncId ? (
          <QuivrButton
            label="Back to connections"
            color="primary"
            iconName="chevronLeft"
            onClick={() => setCurrentSyncId(undefined)}
          />
        ) : (
          <QuivrButton
            label="Previous step"
            color="primary"
            iconName="chevronLeft"
            onClick={goToPreviousStep}
          />
        )}
        {currentSyncId ? (
          <QuivrButton
            label={buttonProps.label}
            color={buttonProps.type}
            iconName={buttonProps.type === "dangerous" ? "delete" : "add"}
            onClick={buttonProps.callback}
            important={true}
            disabled={buttonProps.disabled}
          />
        ) : (
          <QuivrButton
            label={"Next step"}
            color="primary"
            iconName="chevronRight"
            onClick={goToNextStep}
            important={true}
            disabled={
              knowledgeToFeed.length === 0 &&
              !userIdentityData?.onboarded &&
              !openedConnections.length
            }
          />
        )}
      </div>
    );
  };

  if (currentStepIndex !== 1) {
    return <></>;
  }

  return (
    <div className={styles.brain_knowledge_wrapper}>
      {renderFeedBrain()}
      {renderButtons()}
    </div>
  );
};
