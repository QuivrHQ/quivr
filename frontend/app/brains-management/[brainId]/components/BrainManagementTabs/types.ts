export const brainManagementTabs = [
  "settings",
  "people",
  "knowledgeOrSecrets",
] as const;

export type BrainManagementTab = (typeof brainManagementTabs)[number];
