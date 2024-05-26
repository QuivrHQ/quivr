import { useState } from "react";

import { SyncElement } from "@/lib/api/sync/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFromConnections = () => {
  const [currentSyncElements, setCurrentSyncElements] = useState<SyncElement[]>(
    []
  );

  return {
    currentSyncElements,
    setCurrentSyncElements,
  };
};
