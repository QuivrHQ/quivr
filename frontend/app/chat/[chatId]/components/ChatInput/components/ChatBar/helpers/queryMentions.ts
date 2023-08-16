import { BeautifulMentionsItem } from "lexical-beautiful-mentions";

export const triggers = ["@"] as const;

export type Trigger = (typeof triggers)[number];

export const queryMentions = async (
  trigger: string,
  queryString: string | null | undefined,
  mentionItems: Record<Trigger, string[]>
): Promise<BeautifulMentionsItem[]> => {
  await Promise.resolve();

  if (queryString === null || queryString === undefined) {
    return [];
  }

  if (!triggers.includes("@")) {
    return [];
  }

  const items = mentionItems[trigger as Trigger];

  return items
    .filter((item) => {
      return item.toLowerCase().includes(queryString.toLowerCase());
    })
    .map((item) => ({
      value: item,
    }));
};
