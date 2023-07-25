import { useState } from "react";

import { BrainManagementTab } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainManagementTabs = () => {
  const [selectedTab, setSelectedTab] =
    useState<BrainManagementTab>("settings");

  return {
    selectedTab,
    setSelectedTab,
  };
};
