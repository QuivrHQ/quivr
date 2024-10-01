import { createContext, useState } from "react";

import { KMSElement, SyncsByProvider } from "@/lib/api/sync/types";

type KnowledgeContextType = {
  currentFolder: KMSElement | undefined;
  setCurrentFolder: React.Dispatch<
    React.SetStateAction<KMSElement | undefined>
  >;
  quivrRootSelected: boolean;
  setQuivrRootSelected: React.Dispatch<React.SetStateAction<boolean>>;
  providerRootSelected: SyncsByProvider | undefined;
  setProviderRootSelected: React.Dispatch<
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
  const [quivrRootSelected, setQuivrRootSelected] = useState<boolean>(false);
  const [providerRootSelected, setProviderRootSelected] = useState<
    SyncsByProvider | undefined
  >(undefined);

  return (
    <KnowledgeContext.Provider
      value={{
        currentFolder,
        setCurrentFolder,
        quivrRootSelected,
        setQuivrRootSelected,
        providerRootSelected,
        setProviderRootSelected,
      }}
    >
      {children}
    </KnowledgeContext.Provider>
  );
};
