"use client";

import { createContext, useState } from "react";

import { Knowledge } from "@/lib/types/Knowledge";

type KnowledgeContextType = {
  allKnowledge: Knowledge[];
  setAllKnowledge: React.Dispatch<React.SetStateAction<Knowledge[]>>;
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

  return (
    <KnowledgeContext.Provider
      value={{
        allKnowledge,
        setAllKnowledge,
      }}
    >
      {children}
    </KnowledgeContext.Provider>
  );
};
