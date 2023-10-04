"use client";

import { createContext, useState } from "react";

import { OnboardingState } from "./types";

type OnboardingContextType = {
  currentStep: OnboardingState;
  setCurrentStep: React.Dispatch<React.SetStateAction<OnboardingState>>;
};

export const OnboardingContext = createContext<
  OnboardingContextType | undefined
>(undefined);

export const OnboardingContextProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [currentStep, setCurrentStep] = useState<OnboardingState>("DOWNLOAD");

  return (
    <OnboardingContext.Provider
      value={{
        currentStep,
        setCurrentStep,
      }}
    >
      {children}
    </OnboardingContext.Provider>
  );
};
