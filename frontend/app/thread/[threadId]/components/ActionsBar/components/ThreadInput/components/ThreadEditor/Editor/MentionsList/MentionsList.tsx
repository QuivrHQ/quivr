import { SuggestionKeyDownProps } from "@tiptap/suggestion";
import { forwardRef } from "react";

import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import { MentionItem } from "./MentionItem/MentionItem";
import styles from "./MentionsList.module.scss";
import { useMentionList } from "./hooks/useMentionList";
import { MentionListProps } from "./types";

export type MentionListRef = {
  onKeyDown: (event: SuggestionKeyDownProps) => boolean;
};

export const MentionList = forwardRef<MentionListRef, MentionListProps>(
  (props, ref) => {
    const { selectItem, selectedIndex, isBrain } = useMentionList({
      ...props,
      ref,
    });

    const { setIsBrainCreationModalOpened } = useBrainCreationContext();

    const handleClick = (event: React.MouseEvent<HTMLDivElement>) => {
      event.preventDefault();
      event.stopPropagation();
    };

    return (
      <div className={styles.mentions_list_wrapper} onClick={handleClick}>
        <div className={styles.mentions_list}>
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
            <QuivrButton
              label="Create Brain"
              iconName="add"
              color="primary"
              onClick={() => setIsBrainCreationModalOpened(true)}
            />
          )}
        </div>
      </div>
    );
  }
);

MentionList.displayName = "MentionList";
