import { createContext, useState } from "react";

import { KMSElement, SyncsByProvider } from "@/lib/api/sync/types";

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

  return (
    <KnowledgeContext.Provider
      value={{
        currentFolder,
        setCurrentFolder,
        exploringQuivr,
        setExploringQuivr,
        exploredProvider,
        setExploredProvider,
      }}
    >
      {children}
    </KnowledgeContext.Provider>
  );
};
