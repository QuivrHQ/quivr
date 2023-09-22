import { useContext } from "react";

import { KnowledgeContext } from "../knowledge-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeContext = () => {
  const context = useContext(KnowledgeContext);

  if (context === undefined) {
    throw new Error("useKnowledge must be used inside KnowledgeProvider");
  }

  return context;
};
