import { SuggestionKeyDownProps } from "@tiptap/suggestion";
import { forwardRef } from "react";

import { AddBrainModal } from "@/lib/components/AddBrainModal";

import { AddNewPromptButton } from "./components/AddNewPromptButton";
import { MentionItem } from "./components/MentionItem/MentionItem";
import { useMentionList } from "./hooks/useMentionList";
import { MentionListProps } from "./types";

export type MentionListRef = {
  onKeyDown: (event: SuggestionKeyDownProps) => boolean;
};

export const MentionList = forwardRef<MentionListRef, MentionListProps>(
  (props, ref) => {
    const { selectItem, selectedIndex, isBrain, isPrompt } = useMentionList({
      ...props,
      ref,
    });

    return (
      <div className="items flex flex-col p-2 px-4 bg-gray-50 rounded-md shadow-md z-40">
        {props.suggestionData.items.map((item, index) => (
          <MentionItem
            key={item.id}
            item={item}
            isSelected={index === selectedIndex}
            onClick={() => selectItem(index)}
            type={props.suggestionData.type}
          />
        ))}
        {isBrain && <AddBrainModal />}
        {isPrompt && <AddNewPromptButton />}
      </div>
    );
  }
);

MentionList.displayName = "MentionList";
