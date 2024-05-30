import { createContext, useState } from "react";

import { SyncElements } from "@/lib/api/sync/types";

export type FromConnectionsContextType = {
  currentSyncElements: SyncElements | undefined;
  setCurrentSyncElements: React.Dispatch<
    React.SetStateAction<SyncElements | undefined>
  >;
  currentSyncId: number | undefined;
  setCurrentSyncId: React.Dispatch<React.SetStateAction<number | undefined>>;
};

export const FromConnectionsContext = createContext<
  FromConnectionsContextType | undefined
>(undefined);

export const FromConnectionsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [currentSyncElements, setCurrentSyncElements] = useState<
    SyncElements | undefined
  >(undefined);
  const [currentSyncId, setCurrentSyncId] = useState<number | undefined>(
    undefined
  );

  return (
    <FromConnectionsContext.Provider
      value={{
        currentSyncElements,
        setCurrentSyncElements,
        currentSyncId,
        setCurrentSyncId,
      }}
    >
      {children}
    </FromConnectionsContext.Provider>
  );
};
