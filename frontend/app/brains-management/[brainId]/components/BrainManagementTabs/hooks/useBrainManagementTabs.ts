import { UUID } from "crypto";
import { useParams } from "next/navigation";
import { useState } from "react";

import { BrainManagementTab } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainManagementTabs = () => {
  const [selectedTab, setSelectedTab] =
    useState<BrainManagementTab>("settings");

  const params = useParams();

  const brainId = params?.brainId as UUID | undefined;

  return {
    selectedTab,
    setSelectedTab,
    brainId,
  };
};
