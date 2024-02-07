import { BrainManagementTab, brainManagementTabs } from "../types";

export const getTargetedTab = (): BrainManagementTab | undefined => {
  const targetedTab = window.location.hash.split("#")[1];
  if (brainManagementTabs.includes(targetedTab as BrainManagementTab)) {
    return targetedTab as BrainManagementTab;
  }
};
