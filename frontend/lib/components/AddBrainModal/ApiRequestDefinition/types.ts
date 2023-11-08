export const apiTabs = ["searchParams", "headers", "params"] as const;

export type ApiTab = (typeof apiTabs)[number];
