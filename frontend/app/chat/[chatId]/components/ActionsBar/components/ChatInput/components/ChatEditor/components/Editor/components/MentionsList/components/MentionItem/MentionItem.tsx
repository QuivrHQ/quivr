import { cn } from "@/lib/utils";

import { useMentionItemIcon } from "./hooks/useMentionItemIcon";

import { SuggestionDataType, SuggestionItem } from "../../../../types";

type MentionItemProps = {
  item: SuggestionItem;
  type: SuggestionDataType;
  isSelected: boolean;
  onClick: () => void;
};

export const MentionItem = ({
  item,
  isSelected,
  onClick,
  type,
}: MentionItemProps): JSX.Element => {
  const { icon } = useMentionItemIcon({ item, type });

  return (
    <span
      className={cn(
        isSelected ? "bg-msg-purple" : "bg-transparent",
        "hover:text-blue-500",
        "px-3 py-1 rounded-md cursor-pointer flex flex-row gap-1"
      )}
      key={item.id}
      onClick={onClick}
    >
      {icon} {item.label}
    </span>
  );
};
