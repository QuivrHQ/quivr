export const apiTabs = ["params", "searchParams", "secrets"] as const;

export type ApiTab = (typeof apiTabs)[number];
