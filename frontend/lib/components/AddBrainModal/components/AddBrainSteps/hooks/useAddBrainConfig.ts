import { useState } from "react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddBrainConfig = () => {
  const [isBrainCreationModalOpened, setIsBrainCreationModalOpened] =
    useState(false);

  return {
    isBrainCreationModalOpened,
    setIsBrainCreationModalOpened,
  };
};
