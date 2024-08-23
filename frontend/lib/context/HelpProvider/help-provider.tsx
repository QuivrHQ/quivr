import { createContext, useState } from "react";

type HelpContextType = {
  isVisible: boolean;
  setIsVisible: React.Dispatch<React.SetStateAction<boolean>>;
};

export const HelpContext = createContext<HelpContextType | undefined>(
  undefined
);

export const HelpProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <HelpContext.Provider
      value={{
        isVisible,
        setIsVisible,
      }}
    >
      {children}
    </HelpContext.Provider>
  );
};
