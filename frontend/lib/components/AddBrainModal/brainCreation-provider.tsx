import { createContext, useContext, useState } from "react";

import { IntegrationBrains } from "@/lib/api/brain/types";

import { StepValue } from "./types/types";

interface BrainCreationContextProps {
  isBrainCreationModalOpened: boolean;
  setIsBrainCreationModalOpened: React.Dispatch<React.SetStateAction<boolean>>;
  creating: boolean;
  setCreating: React.Dispatch<React.SetStateAction<boolean>>;
  currentSelectedBrain: IntegrationBrains | undefined;
  setCurrentSelectedBrain: React.Dispatch<
    React.SetStateAction<IntegrationBrains | undefined>
  >;
  currentStep: StepValue;
  setCurrentStep: React.Dispatch<React.SetStateAction<StepValue>>;
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
  const [currentSelectedBrain, setCurrentSelectedBrain] =
    useState<IntegrationBrains>();
  const [creating, setCreating] = useState<boolean>(false);
  const [currentStep, setCurrentStep] = useState<StepValue>("FIRST_STEP");

  return (
    <BrainCreationContext.Provider
      value={{
        isBrainCreationModalOpened,
        setIsBrainCreationModalOpened,
        creating,
        setCreating,
        currentSelectedBrain,
        setCurrentSelectedBrain,
        currentStep,
        setCurrentStep,
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
