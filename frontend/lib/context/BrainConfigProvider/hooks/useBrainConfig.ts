/* eslint-disable */
import { useContext } from "react";

import { BrainConfigContext } from "../brain-config-provider";

export const useBrainConfig = () => {
  const context = useContext(BrainConfigContext);

  if (context === undefined) {
    throw new Error("useBrainConfig must be used inside BrainConfigProvider");
  }

  return context;
};
