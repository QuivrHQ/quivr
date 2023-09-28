import { useEffect, useState } from "react";

import { useKnowledgeContext } from "@/lib/context/KnowledgeProvider/hooks/useKnowledgeContext";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSelectedChatPage = () => {
  const [shouldDisplayUploadCard, setShouldDisplayUploadCard] = useState(false);
  const { knowledgeToFeed } = useKnowledgeContext();

  useEffect(() => {
    if (knowledgeToFeed.length > 0 && !shouldDisplayUploadCard) {
      setShouldDisplayUploadCard(true);
    }
  }, [knowledgeToFeed, setShouldDisplayUploadCard]);

  return {
    shouldDisplayUploadCard,
    setShouldDisplayUploadCard,
  };
};
