import { useState } from "react";

import { SyncElements } from "@/lib/api/sync/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFromConnections = () => {
  const [currentSyncElements, setCurrentSyncElements] =
    useState<SyncElements>();

  return {
    currentSyncElements,
    setCurrentSyncElements,
  };
};
