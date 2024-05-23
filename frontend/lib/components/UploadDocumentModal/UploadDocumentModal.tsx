import { useState } from "react";
import { useTranslation } from "react-i18next";

import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

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

  useKnowledgeToFeedContext();
  const { t } = useTranslation(["knowledge"]);

  const handleFeedBrain = async () => {
    setFeeding(true);
    await feedBrain();
    setFeeding(false);
    setShouldDisplayFeedCard(false);
  };

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
        <div className={styles.button}>
          <QuivrButton
            label="Feed Brain"
            color="primary"
            iconName="add"
            onClick={handleFeedBrain}
            disabled={knowledgeToFeed.length === 0 || !currentBrain}
            isLoading={feeding}
            important={true}
          />
        </div>
      </div>
    </Modal>
  );
};
