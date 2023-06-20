"use client";

import { BrainContext } from "./hooks/useBrainContext";
import { useBrainState } from "./hooks/useBrainState";

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
