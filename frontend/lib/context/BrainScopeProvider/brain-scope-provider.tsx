"use client";

import { createContext } from "react";
import _useBrainScopeState from "./hooks/_useBrainScopeState";
import { ScopeContext } from "./types";

export const BrainScopeContext = createContext<ScopeContext | undefined>(
  undefined
);

export const BrainScopeProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const brainState = _useBrainScopeState();

  return (
    <BrainScopeContext.Provider value={brainState}>
      {children}
    </BrainScopeContext.Provider>
  );
};
