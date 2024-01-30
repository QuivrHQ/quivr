import { useTranslation } from "react-i18next";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

export const UploadDocumentButton = (): JSX.Element => {
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { t } = useTranslation("upload");

  return (
    <MenuButton
      iconName="upload"
      label={t("title")}
      type="add"
      onClick={() => setShouldDisplayFeedCard(true)}
    />
  );
};
