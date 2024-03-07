import { SuggestionKeyDownProps } from "@tiptap/suggestion";
import { ForwardedRef, useEffect, useImperativeHandle, useState } from "react";

import { MentionListRef } from "../MentionsList";
import { MentionListProps } from "../types";

type UseMentionListProps = MentionListProps & {
  ref: ForwardedRef<MentionListRef>;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionList = (props: UseMentionListProps) => {
  const [selectedIndex, setSelectedIndex] = useState<number>(0);

  const selectItem = (index: number) => {
    const item = props.suggestionData.items[index];

    if (item !== undefined) {
      props.command(item);
    }
  };

  const upHandler = () => {
    setSelectedIndex(
      (selectedIndex + props.suggestionData.items.length - 1) %
        props.suggestionData.items.length
    );
  };

  const downHandler = () => {
    setSelectedIndex((selectedIndex + 1) % props.suggestionData.items.length);
  };

  const enterHandler = () => {
    selectItem(selectedIndex);
  };

  useEffect(() => setSelectedIndex(0), [props.suggestionData]);

  useImperativeHandle(props.ref, () => ({
    onKeyDown: ({ event }: SuggestionKeyDownProps) => {
      const { key } = event;

      if (key === "ArrowUp") {
        upHandler();

        return true;
      }

      if (key === "ArrowDown") {
        downHandler();

        return true;
      }

      if (key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        event.stopPropagation();
        enterHandler();

        return true;
      }

      return false;
    },
  }));

  const isBrain = props.suggestionData.type === "brain";

  const isPrompt = props.suggestionData.type === "prompt";

  return {
    isBrain,
    selectedIndex,
    selectItem,
    isPrompt,
  };
};
