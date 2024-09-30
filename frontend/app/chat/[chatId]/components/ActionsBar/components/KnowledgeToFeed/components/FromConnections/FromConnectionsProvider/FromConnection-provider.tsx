import { createContext, useState } from "react";

import { KMSElements, OpenedConnection, Provider } from "@/lib/api/sync/types";

export type FromConnectionsContextType = {
  currentKMSElements: KMSElements | undefined;
  setCurrentKMSElements: React.Dispatch<
    React.SetStateAction<KMSElements | undefined>
  >;
  currentSyncId: number | undefined;
  setCurrentSyncId: React.Dispatch<React.SetStateAction<number | undefined>>;
  openedConnections: OpenedConnection[];
  setOpenedConnections: React.Dispatch<
    React.SetStateAction<OpenedConnection[]>
  >;
  hasToReload: boolean;
  setHasToReload: React.Dispatch<React.SetStateAction<boolean>>;
  loadingFirstList: boolean;
  setLoadingFirstList: React.Dispatch<React.SetStateAction<boolean>>;
  currentProvider: Provider | null;
  setCurrentProvider: React.Dispatch<React.SetStateAction<Provider | null>>;
};

export const FromConnectionsContext = createContext<
  FromConnectionsContextType | undefined
>(undefined);

export const FromConnectionsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [currentKMSElements, setCurrentKMSElements] = useState<
    KMSElements | undefined
  >(undefined);
  const [currentSyncId, setCurrentSyncId] = useState<number | undefined>(
    undefined
  );
  const [openedConnections, setOpenedConnections] = useState<
    OpenedConnection[]
  >([]);
  const [currentProvider, setCurrentProvider] = useState<Provider | null>(null);
  const [hasToReload, setHasToReload] = useState<boolean>(false);
  const [loadingFirstList, setLoadingFirstList] = useState<boolean>(false);

  return (
    <FromConnectionsContext.Provider
      value={{
        currentKMSElements,
        setCurrentKMSElements,
        currentSyncId,
        setCurrentSyncId,
        openedConnections,
        setOpenedConnections,

        hasToReload,
        setHasToReload,

        loadingFirstList,
        setLoadingFirstList,

        currentProvider,
        setCurrentProvider,
      }}
    >
      {children}
    </FromConnectionsContext.Provider>
  );
};
