import { createContext, useState } from "react";

import { OpenedConnection, SyncElements } from "@/lib/api/sync/types";

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
  hasToReload: boolean;
  setHasToReload: React.Dispatch<React.SetStateAction<boolean>>;
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
  const [hasToReload, setHasToReload] = useState<boolean>(false);

  return (
    <FromConnectionsContext.Provider
      value={{
        currentSyncElements,
        setCurrentSyncElements,
        currentSyncId,
        setCurrentSyncId,
        openedConnections,
        setOpenedConnections,

        hasToReload,
        setHasToReload,
      }}
    >
      {children}
    </FromConnectionsContext.Provider>
  );
};
