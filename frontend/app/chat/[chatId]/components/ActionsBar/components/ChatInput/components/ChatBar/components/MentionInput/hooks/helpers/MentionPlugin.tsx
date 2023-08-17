import createMentionPlugin from "@draft-js-plugins/mention";
import { useMemo } from "react";

import { BrainMentionItem } from "../../../BrainMentionItem";

interface MentionPluginProps {
  removeMention: (entityKeyToRemove: string) => void;
}

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionPlugin = (props: MentionPluginProps) => {
  const { removeMention } = props;

  const { MentionSuggestions, plugins } = useMemo(() => {
    const mentionPlugin = createMentionPlugin({
      mentionComponent: ({ entityKey, mention: { name } }) => (
        <BrainMentionItem
          text={name}
          onRemove={() => removeMention(entityKey)}
        />
      ),

      popperOptions: {
        placement: "top-end",
      },
    });
    const { MentionSuggestions: coreMentionSuggestions } = mentionPlugin;
    const corePlugins = [mentionPlugin];

    return { plugins: corePlugins, MentionSuggestions: coreMentionSuggestions };
  }, []);

  return { MentionSuggestions, plugins };
};
