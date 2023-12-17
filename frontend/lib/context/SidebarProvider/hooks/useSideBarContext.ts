import { useContext } from "react";

import { SideBarContext } from "../sidebar-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSideBarContext = () => {
  const context = useContext(SideBarContext);
  if (context === undefined) {
    throw new Error("useSideBarContext must be used within a SideBarProvider");
  }

  return context;
};
