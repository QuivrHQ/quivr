import { useContext } from "react";

import { ThreadsContext } from "../threads-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useThreadsContext = () => {
  const context = useContext(ThreadsContext);

  if (context === undefined) {
    throw new Error("useThreadsContext must be used inside ThreadsProvider");
  }

  return context;
};
