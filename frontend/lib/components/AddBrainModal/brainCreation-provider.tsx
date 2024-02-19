import { createContext, useContext, useState } from "react";

import { IntegrationBrains } from "@/lib/api/brain/types";

interface BrainCreationContextProps {
  isBrainCreationModalOpened: boolean;
  setIsBrainCreationModalOpened: React.Dispatch<React.SetStateAction<boolean>>;
  creating: boolean;
  setCreating: React.Dispatch<React.SetStateAction<boolean>>;
  currentIntegrationBrain: IntegrationBrains | undefined;
  setCurrentIntegrationBrain: React.Dispatch<
    React.SetStateAction<IntegrationBrains | undefined>
  >;
}

export const BrainCreationContext = createContext<
  BrainCreationContextProps | undefined
>(undefined);

export const BrainCreationProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isBrainCreationModalOpened, setIsBrainCreationModalOpened] =
    useState<boolean>(false);
  const [currentIntegrationBrain, setCurrentIntegrationBrain] =
    useState<IntegrationBrains>();
  const [creating, setCreating] = useState<boolean>(false);

  return (
    <BrainCreationContext.Provider
      value={{
        isBrainCreationModalOpened,
        setIsBrainCreationModalOpened,
        creating,
        setCreating,
        currentIntegrationBrain,
        setCurrentIntegrationBrain,
      }}
    >
      {children}
    </BrainCreationContext.Provider>
  );
};

export const useBrainCreationContext = (): BrainCreationContextProps => {
  const context = useContext(BrainCreationContext);
  if (!context) {
    throw new Error(
      "useBrainCreationContext must be used within a BrainCreationProvider"
    );
  }

  return context;
};
