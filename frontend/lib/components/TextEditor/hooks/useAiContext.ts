import { useContext } from "react";

import { AiContext, AiContextType } from "../context/AiProvider";

export const useAiContext = (): AiContextType => {
  const value = useContext(AiContext);
  if (value === null) {
    throw new Error("useAiContext must be used within AiProvider");
  }

  return value;
};
