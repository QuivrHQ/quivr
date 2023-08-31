export const brainManagementTabs = ["settings", "people", "knowledge"] as const;

export type BrainManagementTab = (typeof brainManagementTabs)[number];
