import { useEffect, useState } from "react";

import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSelectedChatPage = () => {
  const [shouldDisplayUploadCard, setShouldDisplayUploadCard] = useState(false);
  const { knowledgeToFeed } = useKnowledgeToFeedContext();

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
