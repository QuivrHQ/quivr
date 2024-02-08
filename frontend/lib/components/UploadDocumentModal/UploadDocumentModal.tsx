import { useTranslation } from "react-i18next";

import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import styles from "./UploadDocumentModal.module.scss";

import { Modal } from "../ui/Modal/Modal";

export const UploadDocumentModal = (): JSX.Element => {
  const { shouldDisplayFeedCard, setShouldDisplayFeedCard } =
    useKnowledgeToFeedContext();
  const { t } = useTranslation(["knowledge"]);

  if (!shouldDisplayFeedCard) {
    return <></>;
  }

  return (
    <Modal
      isOpen={shouldDisplayFeedCard}
      setOpen={setShouldDisplayFeedCard}
      title={t("addKnowledgeTitle", { ns: "knowledge" })}
      desc={t("addKnowledgeSubtitle", { ns: "knowledge" })}
      CloseTrigger={<div />}
    >
      <div className={styles.knowledge_modal}>
        <KnowledgeToFeed />
      </div>
    </Modal>
  );
};
