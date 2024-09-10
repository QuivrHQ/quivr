import { createContext, useState } from "react";

type KnowledgeContextType = {
  isVisible: boolean;
  setIsVisible: React.Dispatch<React.SetStateAction<boolean>>;
};

export const KnowledgeContext = createContext<KnowledgeContextType | undefined>(
  undefined
);

export const KnowledgeProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <KnowledgeContext.Provider
      value={{
        isVisible,
        setIsVisible,
      }}
    >
      {children}
    </KnowledgeContext.Provider>
  );
};
