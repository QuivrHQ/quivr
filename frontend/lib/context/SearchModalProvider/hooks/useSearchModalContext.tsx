import { useContext } from "react";

import { SearchModalContext } from "../search-modal-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSearchModalContext = () => {
  const context = useContext(SearchModalContext);
  if (context === undefined) {
    throw new Error("useSearchModalContext must be used within a MenuProvider");
  }

  return context;
};
