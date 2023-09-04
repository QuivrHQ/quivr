import { MentionData } from "@draft-js-plugins/mention";

export const mentionTriggers = ["@"] as const;
export type MentionTriggerType = (typeof mentionTriggers)[number];
export type MentionInputMentionsType = Record<
  MentionTriggerType,
  MentionData[]
>;
