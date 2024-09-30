import { createContext, useState } from "react";

import { KMSElement } from "@/lib/api/sync/types";

type KnowledgeContextType = {
  currentFolder: KMSElement | undefined;
  setCurrentFolder: React.Dispatch<
    React.SetStateAction<KMSElement | undefined>
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
