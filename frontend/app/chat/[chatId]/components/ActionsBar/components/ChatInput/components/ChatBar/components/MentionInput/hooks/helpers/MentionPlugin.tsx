import createMentionPlugin from "@draft-js-plugins/mention";
import { useMemo } from "react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionPlugin = () => {
  const { MentionSuggestions, plugins } = useMemo(() => {
    const mentionPlugin = createMentionPlugin({
      mentionComponent: () => <span />,

      mentionTrigger: ["@", "#"],
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
    const { MentionSuggestions: LegacyMentionSuggestions } = mentionPlugin;
    const legacyPlugins = [mentionPlugin];

    return {
      plugins: legacyPlugins,
      MentionSuggestions: LegacyMentionSuggestions,
    };
  }, []);

  return { MentionSuggestions, plugins };
};
