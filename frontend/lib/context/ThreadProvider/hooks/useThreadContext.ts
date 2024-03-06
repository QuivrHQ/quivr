import { useContext } from "react";

import { ThreadContext } from "../ThreadProvider";
import { ThreadContextProps } from "../types";

export const useThreadContext = (): ThreadContextProps => {
  const context = useContext(ThreadContext);

  if (context === undefined) {
    throw new Error("useThreadContext must be used inside ThreadProvider");
  }

  return context;
};
