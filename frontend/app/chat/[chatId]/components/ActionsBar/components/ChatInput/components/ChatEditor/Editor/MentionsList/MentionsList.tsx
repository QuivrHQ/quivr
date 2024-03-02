import { SuggestionKeyDownProps } from "@tiptap/suggestion";
import { forwardRef } from "react";

import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import TextButton from "@/lib/components/ui/TextButton/TextButton";

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

    const { setIsBrainCreationModalOpened } = useBrainCreationContext();

    const handleClick = (event: React.MouseEvent<HTMLDivElement>) => {
      event.preventDefault();
      event.stopPropagation();
    };

    return (
      <div onClick={handleClick}>
        <div>
          {props.suggestionData.items.map((item, index) => (
            <MentionItem
              key={item.id}
              item={item}
              isSelected={index === selectedIndex}
              onClick={() => selectItem(index)}
              type={props.suggestionData.type}
            />
          ))}
        </div>
        <div>
          {isBrain && (
            <TextButton
              label="Create Brain"
              iconName="add"
              color="black"
              onClick={() => setIsBrainCreationModalOpened(true)}
            />
          )}
          {isPrompt && <AddNewPromptButton />}
        </div>
      </div>
    );
  }
);

MentionList.displayName = "MentionList";
