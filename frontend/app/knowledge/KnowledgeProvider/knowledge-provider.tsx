import { createContext, useState } from "react";

import { SyncElement } from "@/lib/api/sync/types";

type KnowledgeContextType = {
  currentFolder: SyncElement | undefined;
  setCurrentFolder: React.Dispatch<
    React.SetStateAction<SyncElement | undefined>
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
  const [currentFolder, setCurrentFolder] = useState<SyncElement | undefined>(
    undefined
  );

  return (
    <KnowledgeContext.Provider
      value={{
        currentFolder,
        setCurrentFolder,
      }}
    >
      {children}
    </KnowledgeContext.Provider>
  );
};
