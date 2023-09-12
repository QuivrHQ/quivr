import { useContext } from "react";

import { BrainConfigContext } from "@/lib/context/BrainConfigProvider/brain-config-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainConfig = () => {
  const context = useContext(BrainConfigContext);

  if (context === undefined) {
    throw new Error("useBrainConfig must be used inside BrainConfigProvider");
  }

  return context;
};
