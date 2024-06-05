import { useEffect, useState } from "react";

import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { OpenedConnection } from "@/lib/api/sync/types";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
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
    selectSpecificFiles,
    setSelectSpecificFiles,
    openedConnections,
    setOpenedConnections,
  } = useFromConnectionsContext();
  const [currentConnection, setCurrentConnection] = useState<
    OpenedConnection | undefined
  >(undefined);

  useEffect(() => {
    setCurrentConnection(
      openedConnections.find((connection) => connection.id === currentSyncId)
    );
  }, [currentSyncId]);

  const previous = (): void => {
    goToPreviousStep();
  };

  const next = (): void => {
    goToNextStep();
  };

  const isRemoveAll = (): boolean => {
    return !!(
      currentConnection?.allFiles &&
      !selectSpecificFiles &&
      currentConnection.submitted
    );
  };

  const isUpdate = (): boolean => {
    return !!(
      !currentConnection?.allFiles &&
      (selectSpecificFiles ||
        (currentConnection?.submitted && selectSpecificFiles))
    );
  };

  const arraysAreEqual = (arr1: string[], arr2: string[]): boolean => {
    if (arr1.length !== arr2.length) {
      return false;
    }

    for (let i = 0; i < arr1.length; i++) {
      if (arr1[i] !== arr2[i]) {
        return false;
      }
    }

    return true;
  };

  const getButtonProps = (): {
    label: string;
    type: "dangerous" | "primary";
    disabled: boolean;
    callback: () => void;
  } => {
    const matchingOpenedConnection =
      currentConnection &&
      openedConnections.find((conn) => conn.id === currentConnection.id);

    if (matchingOpenedConnection) {
      if (isRemoveAll()) {
        return {
          label: "Remove All",
          type: "dangerous",
          disabled: false,
          callback: removeConnection,
        };
      } else if (
        isUpdate() ||
        (selectSpecificFiles && currentConnection.submitted)
      ) {
        const matchingSelectedFileIds =
          matchingOpenedConnection.selectedFiles.files
            .map((file) => file.id)
            .sort();

        const currentSelectedFileIds = currentConnection.selectedFiles.files
          .map((file) => file.id)
          .sort();

        const isDisabled = arraysAreEqual(
          matchingSelectedFileIds,
          currentSelectedFileIds
        );

        return {
          label: "Update added files",
          type: "primary",
          disabled:
            !matchingOpenedConnection.selectedFiles.files.length || isDisabled,
          callback: addConnection,
        };
      }
    }

    return {
      label: selectSpecificFiles ? "Add specific files" : "Add all",
      type: "primary",
      disabled: false,
      callback: addConnection,
    };
  };

  const addConnection = (): void => {
    setOpenedConnections((prevConnections) => {
      const connectionIndex = prevConnections.findIndex(
        (connection) => connection.id === currentSyncId
      );

      if (connectionIndex !== -1) {
        const newConnections = [...prevConnections];
        newConnections[connectionIndex] = {
          ...newConnections[connectionIndex],
          submitted: true,
        };

        return newConnections;
      }

      return prevConnections;
    });

    setCurrentSyncId(undefined);
    setSelectSpecificFiles(false);
  };

  const removeConnection = (): void => {
    setOpenedConnections((prevConnections) =>
      prevConnections.filter((connection) => connection.id !== currentSyncId)
    );

    setCurrentSyncId(undefined);
    setSelectSpecificFiles(false);
  };

  const renderFeedBrain = () => {
    return (
      <>
        {!userIdentityData?.onboarded && (
          <MessageInfoBox type="tutorial">
            <span>
              Upload documents or add URLs to add knowledges to your brain.
            </span>
          </MessageInfoBox>
        )}
        <div className={styles.feed_brain}>
          <span className={styles.title}>Feed your brain</span>
          <KnowledgeToFeed hideBrainSelector={true} />
        </div>
      </>
    );
  };

  const renderButtons = () => {
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
            onClick={previous}
          />
        )}
        {currentSyncId ? (
          <QuivrButton
            label={getButtonProps().label}
            color={getButtonProps().type}
            iconName={getButtonProps().type === "dangerous" ? "delete" : "add"}
            onClick={getButtonProps().callback}
            important={true}
            disabled={getButtonProps().disabled}
          />
        ) : (
          <QuivrButton
            label={"Next step"}
            color="primary"
            iconName="chevronRight"
            onClick={next}
            important={true}
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
