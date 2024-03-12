import { createContext, useState } from "react";

export type OnboardingContextType = {
  isOnboardingModalOpened: boolean;
  setIsOnboardingModalOpened: React.Dispatch<React.SetStateAction<boolean>>;
};

export const OnboardingContext = createContext<
  OnboardingContextType | undefined
>(undefined);

export const OnboardingProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isOnboardingModalOpened, setIsOnboardingModalOpened] = useState(true);

  return (
    <OnboardingContext.Provider
      value={{
        isOnboardingModalOpened,
        setIsOnboardingModalOpened,
      }}
    >
      {children}
    </OnboardingContext.Provider>
  );
};
