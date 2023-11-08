import { useState } from "react";

import { ApiTab } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useApiDefinitionTabs = () => {
  const [selectedTab, setSelectedTab] = useState<ApiTab>("searchParams");

  return {
    selectedTab,
    setSelectedTab,
  };
};
