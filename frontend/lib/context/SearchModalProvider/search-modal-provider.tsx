import { createContext, useState } from "react";

type SearchModalContextType = {
  isVisible: boolean;
  setIsVisible: React.Dispatch<React.SetStateAction<boolean>>;
};

export const SearchModalContext = createContext<
  SearchModalContextType | undefined
>(undefined);

export const SearchModalProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <SearchModalContext.Provider value={{ isVisible, setIsVisible }}>
      {children}
    </SearchModalContext.Provider>
  );
};
