import { useContext } from "react";

import { KnowledgeContext } from "../knowledge-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeContext = () => {
  const context = useContext(KnowledgeContext);
  if (context === undefined) {
    throw new Error(
      "useKnowledgeContext must be used within a KnowledgeProvider"
    );
  }

  return context;
};
