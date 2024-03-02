import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useMentionConfig } from "./useMentionConfig";

import { SuggestionItem } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePromptMention = () => {
  const { publicPrompts } = useBrainContext();

  const items: SuggestionItem[] = publicPrompts.map((prompt) => ({
    id: prompt.id,
    label: prompt.title,
    type: "prompt",
  }));

  const { Mention: PromptMention } = useMentionConfig({
    char: "#",
    suggestionData: {
      type: "prompt",
      items,
    },
  });

  return {
    PromptMention,
  };
};
