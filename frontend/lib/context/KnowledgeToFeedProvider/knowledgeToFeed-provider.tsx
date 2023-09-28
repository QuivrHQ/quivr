"use client";

import { createContext, useState } from "react";

import { FeedItemType } from "@/app/chat/[chatId]/components/ActionsBar/types";

type KnowledgeToFeedContextType = {
  knowledgeToFeed: FeedItemType[];
  setKnowledgeToFeed: React.Dispatch<React.SetStateAction<FeedItemType[]>>;
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

  return (
    <KnowledgeToFeedContext.Provider
      value={{
        knowledgeToFeed,
        setKnowledgeToFeed,
      }}
    >
      {children}
    </KnowledgeToFeedContext.Provider>
  );
};
