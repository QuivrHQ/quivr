import Image from "next/image";

import styles from "./MentionItem.module.scss";
import { useMentionItemIcon } from "./hooks/useMentionItemIcon";

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
  type,
}: MentionItemProps): JSX.Element => {
  const { icon } = useMentionItemIcon({ item, type });

  return (
    <span
      className={styles.mention_item_wrapper}
      key={item.id}
      onClick={onClick}
    >
      {item.iconUrl && <Image src={item.iconUrl} width={20} alt="hey" />}
      {icon} {item.label}
    </span>
  );
};
