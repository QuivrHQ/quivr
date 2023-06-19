import { createContext, useContext } from "react";

import { BrainStateProps } from "./useBrainState";
import { ScopeContext } from "../types";

export const BrainContext = createContext<ScopeContext | undefined>(undefined);

export const useBrainContext = (): BrainStateProps => {
  const context = useContext(BrainContext);

  if (context === undefined) {
    throw new Error("useBrainContext must be used inside BrainProvider");
  }

  return context;
};
