import { useContext } from "react";

import { FeedItemType } from "@/app/chat/[chatId]/components/ActionsBar/types";

import { KnowledgeContext } from "../knowledge-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeContext = () => {
  const context = useContext(KnowledgeContext);

  const addKnowledgeToFeed = (knowledge: FeedItemType) => {
    context?.setKnowledgeToFeed((prevKnowledge) => [
      ...prevKnowledge,
      knowledge,
    ]);
  };

  const removeKnowledgeToFeed = (index: number) => {
    context?.setKnowledgeToFeed((prevKnowledge) => {
      const newKnowledge = [...prevKnowledge];
      newKnowledge.splice(index, 1);

      return newKnowledge;
    });
  };

  if (context === undefined) {
    throw new Error("useKnowledge must be used inside KnowledgeProvider");
  }

  return { ...context, addKnowledgeToFeed, removeKnowledgeToFeed };
};
