import { useTranslation } from "react-i18next";
import { LuChevronRight, LuFilePlus } from "react-icons/lu";

import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import { Button } from "./Button";

export const FeedCardTrigger = (): JSX.Element => {
  const { t } = useTranslation("chat");
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();

  return (
    <Button
      label={t("add_document")}
      startIcon={<LuFilePlus size={18} />}
      endIcon={<LuChevronRight size={18} />}
      className="w-full"
      onClick={() => setShouldDisplayFeedCard(true)}
    />
  );
};
