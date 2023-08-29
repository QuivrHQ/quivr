export const mentionTriggers = ["@", "#"] as const;

export type MentionTriggerType = (typeof mentionTriggers)[number];
