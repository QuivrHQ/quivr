import { createContext, useState } from "react";

type UserSettingsContextYpe = {
  isDarkMode: boolean;
  setIsDarkMode: React.Dispatch<React.SetStateAction<boolean>>;
};

export const UserSettingsContext = createContext<
  UserSettingsContextYpe | undefined
>(undefined);

export const UserSettingsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);

  return (
    <UserSettingsContext.Provider
      value={{
        isDarkMode,
        setIsDarkMode,
      }}
    >
      {children}
    </UserSettingsContext.Provider>
  );
};
