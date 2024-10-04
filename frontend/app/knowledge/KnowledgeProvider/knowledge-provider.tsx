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
      }}
    >
      {children}
    </KnowledgeContext.Provider>
  );
};
