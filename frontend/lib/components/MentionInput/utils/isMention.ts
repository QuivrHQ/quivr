import { mentionTriggers } from "@/app/chat/[chatId]/components/ActionsBar/types";

const mentionsTags = [
  "mention",
  ...mentionTriggers.map((trigger) => `${trigger}mention`),
];

export const isMention = (type?: string): boolean =>
  type !== undefined && mentionsTags.includes(type);
