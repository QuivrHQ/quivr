const brainTabs = ["all", "private", "public"] as const;
export type BrainTab = (typeof brainTabs)[number];
