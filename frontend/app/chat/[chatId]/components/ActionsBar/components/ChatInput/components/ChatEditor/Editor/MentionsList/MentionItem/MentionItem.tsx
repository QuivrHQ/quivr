import Image from "next/image";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./MentionItem.module.scss";

import { SuggestionDataType, SuggestionItem } from "../../types";

type MentionItemProps = {
  item: SuggestionItem;
  type: SuggestionDataType;
  isSelected: boolean;
  onClick: () => void;
};

export const MentionItem = ({
  item,
  onClick,
}: MentionItemProps): JSX.Element => {
  return (
    <span
      className={styles.mention_item_wrapper}
      key={item.id}
      onClick={onClick}
    >
      {item.iconUrl ? (
        <Image src={item.iconUrl} width={18} height={18} alt="hey" />
      ) : (
        <Icon color="primary" size="normal" name="brain" />
      )}
      {item.label}
    </span>
  );
};
