import { createContext, useState } from "react";

import { Provider, SyncElements } from "@/lib/api/sync/types";

export interface OpenedConnection {
  id: number;
  provider: Provider;
  submitted: boolean;
  allFiles: boolean;
  selectedFiles: string[];
}

export type FromConnectionsContextType = {
  currentSyncElements: SyncElements | undefined;
  setCurrentSyncElements: React.Dispatch<
    React.SetStateAction<SyncElements | undefined>
  >;
  currentSyncId: number | undefined;
  setCurrentSyncId: React.Dispatch<React.SetStateAction<number | undefined>>;
  openedConnections: OpenedConnection[];
  setOpenedConnections: React.Dispatch<
    React.SetStateAction<OpenedConnection[]>
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
  const [currentSyncId, setCurrentSyncId] = useState<number | undefined>(
    undefined
  );
  const [openedConnections, setOpenedConnections] = useState<
    OpenedConnection[]
  >([]);

  return (
    <FromConnectionsContext.Provider
      value={{
        currentSyncElements,
        setCurrentSyncElements,
        currentSyncId,
        setCurrentSyncId,
        openedConnections,
        setOpenedConnections,
      }}
    >
      {children}
    </FromConnectionsContext.Provider>
  );
};
