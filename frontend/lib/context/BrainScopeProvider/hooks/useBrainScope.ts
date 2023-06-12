import { useContext } from "react";
import { BrainScopeContext } from "../brain-scope-provider";

export const useBrainScope = () => {
  const context = useContext(BrainScopeContext);

  if (context === undefined) {
    throw new Error("useBrainScope must be used inside BrainScopeProvider");
  }

  return context;
};
