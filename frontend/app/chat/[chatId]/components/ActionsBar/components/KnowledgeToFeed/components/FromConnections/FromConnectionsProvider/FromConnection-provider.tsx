import { createContext, useState } from "react";

import { SyncElements } from "@/lib/api/sync/types";

export type FromConnectionsContextType = {
  currentSyncElements: SyncElements | undefined;
  setCurrentSyncElements: React.Dispatch<
    React.SetStateAction<SyncElements | undefined>
  >;
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

  return (
    <FromConnectionsContext.Provider
      value={{
        currentSyncElements,
        setCurrentSyncElements,
      }}
    >
      {children}
    </FromConnectionsContext.Provider>
  );
};
