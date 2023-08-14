export const mentionItems: Record<Trigger, string[]> = {
  "@": ["Anton", "Boris", "Catherine", "Dmitri", "Elena", "Felix", "Gina"],
};

export type Trigger = "@";

export const queryMentions = (
  trigger: Trigger,
  queryString: string | null
): string[] => {
  if (queryString === null) {
    return mentionItems[trigger];
  }
  const items = mentionItems[trigger];

  return items.filter((item) => {
    return item.toLowerCase().includes(queryString.toLowerCase());
  });
};
