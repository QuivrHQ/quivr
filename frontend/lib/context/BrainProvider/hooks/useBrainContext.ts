import { useContext } from "react";

import { BrainContext } from "../brain-provider";
import { BrainContextType } from "../types";

export const useBrainContext = (): BrainContextType => {
  const context = useContext(BrainContext);

  if (context === undefined) {
    throw new Error("useBrainContext must be used inside BrainProvider");
  }

  return context;
};
