"use client";

import { createContext } from "react";

import { useBrainState } from "./hooks/useBrainState";
import { BrainContextType } from "./types";

export const BrainContext = createContext<BrainContextType | undefined>(
  undefined
);

export const BrainProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const brainState = useBrainState();

  return (
    <BrainContext.Provider value={brainState}>{children}</BrainContext.Provider>
  );
};
