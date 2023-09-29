"use client";

import { createContext, useState } from "react";

import { FeedItemType } from "@/app/chat/[chatId]/components/ActionsBar/types";

type KnowledgeToFeedContextType = {
  knowledgeToFeed: FeedItemType[];
  setKnowledgeToFeed: React.Dispatch<React.SetStateAction<FeedItemType[]>>;
  shouldDisplayFeedCard: boolean;
  setShouldDisplayFeedCard: React.Dispatch<React.SetStateAction<boolean>>;
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
  const [shouldDisplayFeedCard, setShouldDisplayFeedCard] = useState(false);

  return (
    <KnowledgeToFeedContext.Provider
      value={{
        knowledgeToFeed,
        setKnowledgeToFeed,
        shouldDisplayFeedCard,
        setShouldDisplayFeedCard,
      }}
    >
      {children}
    </KnowledgeToFeedContext.Provider>
  );
};
