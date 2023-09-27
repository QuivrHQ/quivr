"use client";

import { createContext, useState } from "react";

import { FeedItemType } from "@/app/chat/[chatId]/components/ActionsBar/types";
import { Knowledge } from "@/lib/types/Knowledge";

type KnowledgeContextType = {
  allKnowledge: Knowledge[];
  setAllKnowledge: React.Dispatch<React.SetStateAction<Knowledge[]>>;
  knowledgeToFeed: FeedItemType[];
  setKnowledgeToFeed: React.Dispatch<React.SetStateAction<FeedItemType[]>>;
};

export const KnowledgeContext = createContext<KnowledgeContextType | undefined>(
  undefined
);

export const KnowledgeProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [allKnowledge, setAllKnowledge] = useState<Knowledge[]>([]);
  const [knowledgeToFeed, setKnowledgeToFeed] = useState<FeedItemType[]>([]);

  return (
    <KnowledgeContext.Provider
      value={{
        allKnowledge,
        setAllKnowledge,
        knowledgeToFeed,
        setKnowledgeToFeed,
      }}
    >
      {children}
    </KnowledgeContext.Provider>
  );
};
