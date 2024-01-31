import { useTranslation } from "react-i18next";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { Modal } from "@/lib/components/ui/Modal";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

export const UploadDocumentButton = (): JSX.Element => {
  const { shouldDisplayFeedCard, setShouldDisplayFeedCard } =
    useKnowledgeToFeedContext();
  const { t } = useTranslation("upload");

  return (
    <Modal
      Trigger={
        <div onClick={() => void 0}>
          <MenuButton
            iconName="upload"
            label={t("title")}
            type="add"
            onClick={() => setShouldDisplayFeedCard(true)}
            color="primary"
          />
        </div>
      }
      title={t("title", { ns: "upload" })}
      isOpen={shouldDisplayFeedCard}
      setOpen={setShouldDisplayFeedCard}
      CloseTrigger={<div />}
    >
      <UploadDocumentModal />
    </Modal>
  );
};
