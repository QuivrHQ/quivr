"use client";

import { createContext, useState } from "react";

import { FeedItemType } from "@/app/chat/[chatId]/components/ActionsBar/types";

type KnowledgeToFeedContextType = {
  knowledgeToFeed: FeedItemType[];
  setKnowledgeToFeed: React.Dispatch<React.SetStateAction<FeedItemType[]>>;
  shouldDisplayUploadCard: boolean;
  setShouldDisplayUploadCard: React.Dispatch<React.SetStateAction<boolean>>;
};

export const KnowledgeToFeedContext = createContext<
  KnowledgeToFeedContextType | undefined
>(undefined);

export const KnowledgeToFeedProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [knowledgeToFeed, setKnowledgeToFeed] = useState<FeedItemType[]>([]);
  const [shouldDisplayUploadCard, setShouldDisplayUploadCard] = useState(false);

  return (
    <KnowledgeToFeedContext.Provider
      value={{
        knowledgeToFeed,
        setKnowledgeToFeed,
        shouldDisplayUploadCard,
        setShouldDisplayUploadCard,
      }}
    >
      {children}
    </KnowledgeToFeedContext.Provider>
  );
};
