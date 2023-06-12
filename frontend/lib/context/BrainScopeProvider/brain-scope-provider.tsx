"use client";

import { setEmptyStringsUndefined } from "@/lib/helpers/setEmptyStringsUndefined";
import { createContext, useEffect, useState } from "react";
import { BrainScope, ScopeContext } from "./types";
import _useBrainScopeState from "./hooks/_useBrainScopeState";

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
