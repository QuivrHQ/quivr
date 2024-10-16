import { createContext, useState } from "react";

import { KMSElement, Sync, SyncsByProvider } from "@/lib/api/sync/types";

type KnowledgeContextType = {
  currentFolder: KMSElement | undefined;
  setCurrentFolder: React.Dispatch<
    React.SetStateAction<KMSElement | undefined>
  >;
  exploringQuivr: boolean;
  setExploringQuivr: React.Dispatch<React.SetStateAction<boolean>>;
  exploredProvider: SyncsByProvider | undefined;
  setExploredProvider: React.Dispatch<
    React.SetStateAction<SyncsByProvider | undefined>
  >;
  exploredSpecificAccount: Sync | undefined;
  setExploredSpecificAccount: React.Dispatch<
    React.SetStateAction<Sync | undefined>
  >;
  selectedKnowledges: KMSElement[];
  setSelectedKnowledges: React.Dispatch<React.SetStateAction<KMSElement[]>>;
  refetchFolderMenu: boolean;
  setRefetchFolderMenu: React.Dispatch<React.SetStateAction<boolean>>;
  refetchFolderExplorer: boolean;
  setRefetchFolderExplorer: React.Dispatch<React.SetStateAction<boolean>>;
};

export const KnowledgeContext = createContext<KnowledgeContextType | undefined>(
  undefined
);

export const KnowledgeProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [currentFolder, setCurrentFolder] = useState<KMSElement | undefined>(
    undefined
  );
  const [exploringQuivr, setExploringQuivr] = useState<boolean>(false);
  const [exploredProvider, setExploredProvider] = useState<
    SyncsByProvider | undefined
  >(undefined);
  const [exploredSpecificAccount, setExploredSpecificAccount] = useState<
    Sync | undefined
  >(undefined);
  const [selectedKnowledges, setSelectedKnowledges] = useState<KMSElement[]>(
    []
  );
  const [refetchFolderMenu, setRefetchFolderMenu] = useState<boolean>(false);
  const [refetchFolderExplorer, setRefetchFolderExplorer] =
    useState<boolean>(false);

  return (
    <KnowledgeContext.Provider
      value={{
        currentFolder,
        setCurrentFolder,
        exploringQuivr,
        setExploringQuivr,
        exploredProvider,
        setExploredProvider,
        exploredSpecificAccount,
        setExploredSpecificAccount,
        selectedKnowledges,
        setSelectedKnowledges,
        refetchFolderMenu,
        setRefetchFolderMenu,
        refetchFolderExplorer,
        setRefetchFolderExplorer,
      }}
    >
      {children}
    </KnowledgeContext.Provider>
  );
};
