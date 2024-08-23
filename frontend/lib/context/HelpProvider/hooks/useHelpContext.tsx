import { useContext } from "react";

import { HelpContext } from "../help-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useHelpContext = () => {
  const context = useContext(HelpContext);
  if (context === undefined) {
    throw new Error("useHelpContext must be used within a HelpProvider");
  }

  return context;
};
