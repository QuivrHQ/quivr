import { createContext, useContext, useState } from "react";

interface BrainCreationContextProps {
  isBrainCreationModalOpened: boolean;
  setIsBrainCreationModalOpened: React.Dispatch<React.SetStateAction<boolean>>;
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
    useState(false);

  return (
    <BrainCreationContext.Provider
      value={{ isBrainCreationModalOpened, setIsBrainCreationModalOpened }}
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
