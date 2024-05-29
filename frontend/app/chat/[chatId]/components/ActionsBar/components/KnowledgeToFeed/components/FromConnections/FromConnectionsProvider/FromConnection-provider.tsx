import { createContext, useState } from "react";

import { Provider, SyncElements } from "@/lib/api/sync/types";

export type FromConnectionsContextType = {
  currentSyncElements: SyncElements | undefined;
  setCurrentSyncElements: React.Dispatch<
    React.SetStateAction<SyncElements | undefined>
  >;
  currentProvider: Provider | undefined;
  setCurrentProvider: React.Dispatch<
    React.SetStateAction<Provider | undefined>
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
  const [currentProvider, setCurrentProvider] = useState<Provider | undefined>(
    undefined
  );

  return (
    <FromConnectionsContext.Provider
      value={{
        currentSyncElements,
        setCurrentSyncElements,
        currentProvider,
        setCurrentProvider,
      }}
    >
      {children}
    </FromConnectionsContext.Provider>
  );
};
