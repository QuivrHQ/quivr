import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { OpenedConnection } from "@/lib/api/sync/types";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { createHandleGetButtonProps } from "@/lib/helpers/handleConnectionButtons";

import styles from "./UploadDocumentModal.module.scss";
import { useAddKnowledge } from "./hooks/useAddKnowledge";

import { Modal } from "../ui/Modal/Modal";
import { QuivrButton } from "../ui/QuivrButton/QuivrButton";

export const UploadDocumentModal = (): JSX.Element => {
  const { shouldDisplayFeedCard, setShouldDisplayFeedCard, knowledgeToFeed } =
    useKnowledgeToFeedContext();
  const { currentBrain } = useBrainContext();
  const { feedBrain } = useAddKnowledge();
  const [feeding, setFeeding] = useState<boolean>(false);
  const {
    currentSyncId,
    setCurrentSyncId,
    openedConnections,
    setOpenedConnections,
  } = useFromConnectionsContext();
  const [currentConnection, setCurrentConnection] = useState<
    OpenedConnection | undefined
  >(undefined);

  useKnowledgeToFeedContext();
  const { t } = useTranslation(["knowledge"]);

  const handleFeedBrain = async () => {
    setFeeding(true);
    await feedBrain();
    setFeeding(false);
    setShouldDisplayFeedCard(false);
  };

  const getButtonProps = createHandleGetButtonProps(
    currentConnection,
    openedConnections,
    setOpenedConnections,
    currentSyncId,
    setCurrentSyncId
  );
  const buttonProps = getButtonProps();

  useEffect(() => {
    setCurrentConnection(
      openedConnections.find((connection) => connection.id === currentSyncId)
    );
  }, [currentSyncId]);

  if (!shouldDisplayFeedCard) {
    return <></>;
  }

  return (
    <Modal
      isOpen={shouldDisplayFeedCard}
      setOpen={setShouldDisplayFeedCard}
      title={t("addKnowledgeTitle", { ns: "knowledge" })}
      desc={t("addKnowledgeSubtitle", { ns: "knowledge" })}
      size="big"
      CloseTrigger={<div />}
    >
      <div className={styles.knowledge_modal}>
        <KnowledgeToFeed />
        <div
          className={`${styles.buttons} ${
            !currentSyncId ? styles.standalone : ""
          }`}
        >
          {!!currentSyncId && (
            <QuivrButton
              label="Back to connections"
              color="primary"
              iconName="chevronLeft"
              onClick={() => {
                setCurrentSyncId(undefined);
              }}
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
              label="Feed Brain"
              color="primary"
              iconName="add"
              onClick={handleFeedBrain}
              disabled={knowledgeToFeed.length === 0 || !currentBrain}
              isLoading={feeding}
              important={true}
            />
          )}
        </div>
      </div>
    </Modal>
  );
};
