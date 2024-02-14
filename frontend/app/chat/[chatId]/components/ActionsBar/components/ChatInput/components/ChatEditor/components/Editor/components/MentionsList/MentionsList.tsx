import { SuggestionKeyDownProps } from "@tiptap/suggestion";
import { forwardRef } from "react";
import { FaAngleDoubleDown } from "react-icons/fa";

import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import TextButton from "@/lib/components/ui/TextButton/TextButton";

import { AddNewPromptButton } from "./components/AddNewPromptButton";
import { MentionItem } from "./components/MentionItem/MentionItem";
import { useMentionList } from "./hooks/useMentionList";
import { useSuggestionsOverflowHandler } from "./hooks/useSuggestionsOverflowHandler";
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

    const { suggestionsRef, shouldShowScrollToBottomIcon, scrollToBottom } =
      useSuggestionsOverflowHandler();
    const { setIsBrainCreationModalOpened } = useBrainCreationContext();

    const handleClick = (event: React.MouseEvent<HTMLDivElement>) => {
      event.preventDefault();
      event.stopPropagation();
    };

    return (
      <div
        className="items flex flex-1 flex-col p-2 px-4 bg-gray-50 rounded-md shadow-md z-40 max-h-[200px]"
        onClick={handleClick}
      >
        <div
          className="flex flex-1 flex-col overflow-y-auto"
          ref={suggestionsRef}
        >
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
        <div className="relative flex justify-center items-center py-1">
          {shouldShowScrollToBottomIcon && (
            <FaAngleDoubleDown
              size={20}
              className="animate-bounce cursor-pointer absolute right-1 top-0 hover:text-primary"
              onClick={scrollToBottom}
            />
          )}
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
