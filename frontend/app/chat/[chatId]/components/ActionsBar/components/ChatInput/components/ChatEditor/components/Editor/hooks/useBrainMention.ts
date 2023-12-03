import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useMentionConfig } from "./useMentionConfig";
import { SuggestionItem } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainMention = () => {
  const { allBrains } = useBrainContext();

  const items: SuggestionItem[] = allBrains.map((brain) => ({
    id: brain.id,
    label: brain.name,
    type: "brain",
  }));

  const { Mention: BrainMention } = useMentionConfig({
    char: "@",
    suggestionData: {
      type: "brain",
      items,
    },
  });

  return {
    BrainMention,
    items,
  };
};
