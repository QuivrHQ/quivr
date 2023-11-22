import { useState } from "react";

import { ApiTab } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useApiRequestDefinition = () => {
  const [selectedTab, setSelectedTab] = useState<ApiTab>("params");

  return {
    selectedTab,
    setSelectedTab,
  };
};
