import { useContext } from "react";

import { UserSettingsContext } from "../User-settings.provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useUserSettingsContext = () => {
  const context = useContext(UserSettingsContext);
  if (context === undefined) {
    throw new Error(
      "useUserSettingsContext must be used within a UserSettingsProvider"
    );
  }

  return context;
};
