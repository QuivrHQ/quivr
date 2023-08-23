import createMentionPlugin from "@draft-js-plugins/mention";
import { useMemo } from "react";

import { MentionTriggerType } from "@/app/chat/[chatId]/components/ActionsBar/types";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionItem } from "../../../MentionItem";

interface MentionPluginProps {
  removeMention: (entityKeyToRemove: string) => void;
}

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionPlugin = (props: MentionPluginProps) => {
  const { removeMention } = props;
  const { setCurrentBrainId, setCurrentPromptId } = useBrainContext();

  const { BrainMentionSuggestions, PromptMentionSuggestions, plugins } =
    useMemo(() => {
      const brainMentionPlugin = createMentionPlugin({
        mentionComponent: ({ entityKey, mention: { name, trigger } }) => (
          <MentionItem
            text={name}
            onRemove={() => {
              setCurrentBrainId(null);
              removeMention(entityKey);
            }}
            trigger={trigger as MentionTriggerType}
          />
        ),
        mentionPrefix: "@",
        popperOptions: {
          placement: "top-end",
          modifiers: [
            {
              name: "customStyle", // Custom modifier for applying styles
              enabled: true,
              phase: "beforeWrite",
              fn: ({ state }) => {
                state.styles.popper = {
                  ...state.styles.popper,
                  minWidth: "auto",
                  backgroundColor: "transparent",
                  padding: "0",
                  marginBottom: "5",
                };
              },
            },
          ],
        },
      });
      const promptMentionPlugin = createMentionPlugin({
        mentionComponent: ({ entityKey, mention: { name, trigger } }) => (
          <MentionItem
            text={name}
            onRemove={() => {
              setCurrentPromptId(null);
              removeMention(entityKey);
            }}
            trigger={trigger as MentionTriggerType}
          />
        ),
        mentionPrefix: "#",
        mentionTrigger: ["#"],
        popperOptions: {
          placement: "top-end",
          modifiers: [
            {
              name: "customStyle", // Custom modifier for applying styles
              enabled: true,
              phase: "beforeWrite",
              fn: ({ state }) => {
                state.styles.popper = {
                  ...state.styles.popper,
                  minWidth: "auto",
                  backgroundColor: "transparent",
                  padding: "0",
                  marginBottom: "5",
                };
              },
            },
          ],
        },
      });
      const { MentionSuggestions: LegacyBrainMentionSuggestions } =
        brainMentionPlugin;
      const { MentionSuggestions: LegacyPromptMentionSuggestions } =
        promptMentionPlugin;
      const legacyPlugins = [brainMentionPlugin, promptMentionPlugin];

      return {
        plugins: legacyPlugins,
        BrainMentionSuggestions: LegacyBrainMentionSuggestions,
        PromptMentionSuggestions: LegacyPromptMentionSuggestions,
      };
    }, []);

  return { BrainMentionSuggestions, PromptMentionSuggestions, plugins };
};
