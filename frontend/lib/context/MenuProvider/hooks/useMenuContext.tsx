import { useContext } from "react";

import { MenuContext } from "../Menu-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMenuContext = () => {
  const context = useContext(MenuContext);
  if (context === undefined) {
    throw new Error("useMenuContext must be used within a MenuProvider");
  }

  return context;
};
