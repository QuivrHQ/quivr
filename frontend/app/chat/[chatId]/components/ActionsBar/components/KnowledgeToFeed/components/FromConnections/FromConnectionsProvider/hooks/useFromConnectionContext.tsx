import { useContext } from "react";

import {
  FromConnectionsContext,
  FromConnectionsContextType,
} from "../FromConnection-provider";

export const useFromConnectionsContext = (): FromConnectionsContextType => {
  const context = useContext(FromConnectionsContext);
  if (context === undefined) {
    throw new Error(
      "useFromConnectionsContext must be used within a FromConnectionsProvider"
    );
  }

  return context;
};
