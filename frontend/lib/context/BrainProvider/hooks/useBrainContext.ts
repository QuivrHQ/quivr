import { useContext } from "react";

import { BrainStateProps } from "./useBrainState";
import { BrainContext } from "../brain-provider";

export const useBrainContext = (): BrainStateProps => {
  const context = useContext(BrainContext);

  if (context === undefined) {
    throw new Error("useBrainContext must be used inside BrainProvider");
  }

  return context;
};
