import { default as TiptapMention } from "@tiptap/extension-mention";
import { PluginKey } from "@tiptap/pm/state";
import { ReactRenderer } from "@tiptap/react";
import { SuggestionOptions } from "@tiptap/suggestion";
import { RefAttributes, useMemo } from "react";
import tippy, { Instance } from "tippy.js";

import { MentionList, MentionListRef } from "../MentionsList/MentionsList";
import { MentionListProps } from "../MentionsList/types";
import { SuggestionData, SuggestionItem } from "../types";

type UseMentionConfigProps = {
  char: string;
  suggestionData: SuggestionData;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionConfig = ({
  char,
  suggestionData,
}: UseMentionConfigProps) => {
  const mentionKey = `mention${char}`;
  const items = suggestionData.items;

  const suggestionsConfig = useMemo<
    Omit<SuggestionOptions<SuggestionItem>, "editor">
  >(
    () => ({
      char,
      allowSpaces: true,
      pluginKey: new PluginKey(mentionKey),
      items: ({ query }) =>
        items.filter((item) =>
          item.label.toLowerCase().startsWith(query.toLowerCase())
        ),
      render: () => {
        let reactRenderer:
          | ReactRenderer<
              MentionListRef,
              MentionListProps & RefAttributes<MentionListRef>
            >
          | undefined;
        let popup: Instance[] | undefined;

        return {
          onStart: (props) => {
            if (!props.clientRect) {
              return;
            }
            reactRenderer = new ReactRenderer(MentionList, {
              props: {
                ...props,
                suggestionData: {
                  ...suggestionData,
                  items: props.items,
                },
              },
              editor: props.editor,
            });
            popup = tippy("body", {
              zIndex: 1020,
              getReferenceClientRect: () => {
                const rect = props.clientRect?.();

                return rect ? rect : new DOMRect(0, 0, 0, 0);
              },
              appendTo: () => document.body,
              content: reactRenderer.element,
              showOnCreate: true,
              interactive: true,
              trigger: "manual",
              placement: "top-start",
            });
          },
          onUpdate: (props) => {
            reactRenderer?.updateProps({
              ...props,
              suggestionData: {
                ...suggestionData,
                items: props.items,
              },
            });
          },
          onKeyDown: (props) => {
            if (props.event.key === "Escape") {
              popup?.[0].hide();

              return true;
            }

            return reactRenderer?.ref?.onKeyDown(props) ?? false;
          },
          onExit: () => {
            popup?.[0].destroy();
            reactRenderer?.destroy();
          },
        };
      },
    }),
    [char, items, mentionKey, suggestionData]
  );

  const Mention = TiptapMention.extend({
    name: mentionKey,
  }).configure({
    HTMLAttributes: {
      class: "mention",
    },
    suggestion: suggestionsConfig,
    renderLabel: () => {
      return "";
    },
  });

  return {
    Mention,
  };
};
