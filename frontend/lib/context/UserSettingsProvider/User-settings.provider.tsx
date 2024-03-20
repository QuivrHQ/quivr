import { createContext, useEffect, useState } from "react";

type UserSettingsContextType = {
  isDarkMode: boolean;
  setIsDarkMode: React.Dispatch<React.SetStateAction<boolean>>;
};

export const UserSettingsContext = createContext<
  UserSettingsContextType | undefined
>(undefined);

export const UserSettingsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);

  const checkPreferredColorScheme = () => {
    const prefersDarkMode = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    setIsDarkMode(prefersDarkMode);
    prefersDarkMode
      ? document.body.classList.add("dark_mode")
      : document.body.classList.remove("dark_mode");
  };

  useEffect(() => {
    checkPreferredColorScheme();
    const mediaQueryList = window.matchMedia("(prefers-color-scheme: dark)");
    const listener = (event: MediaQueryListEvent) => {
      setIsDarkMode(event.matches);
    };
    mediaQueryList.addEventListener("change", listener);

    return () => {
      mediaQueryList.removeEventListener("change", listener);
    };
  }, []);

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
