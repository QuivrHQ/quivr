import { useContext } from "react";

import { ConfigurationContext } from "../ConfigurationProvider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useConfiguration = () => {
  const context = useContext(ConfigurationContext);
  if (context === undefined) {
    throw new Error(
      "useConfiguration must be used within a ConfigurationProvider"
    );
  }

  return context;
};
