import { createContext, useState } from "react";

export type AssistantContextType = {
  isAssistantModalOpened: boolean;
  setisAssistantModalOpened: React.Dispatch<React.SetStateAction<boolean>>;
};

export const AssistantContext = createContext<AssistantContextType | undefined>(
  undefined
);

export const AssistantProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isAssistantModalOpened, setisAssistantModalOpened] = useState(false);

  return (
    <AssistantContext.Provider
      value={{
        isAssistantModalOpened,
        setisAssistantModalOpened,
      }}
    >
      {children}
    </AssistantContext.Provider>
  );
};
