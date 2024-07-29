import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./MentionItem.module.scss";

import { SuggestionItem } from "../../types";

type MentionItemProps = {
  item: SuggestionItem;
  onClick: () => void;
  selected: boolean;
};

export const MentionItem = ({
  item,
  onClick,
  selected,
}: MentionItemProps): JSX.Element => {
  return (
    <span
      className={`${styles.mention_item_wrapper} ${
        selected ? styles.selected : ""
      }`}
      key={item.id}
      onClick={onClick}
    >
      <Icon name="brain" size="normal" color={selected ? "primary" : "black"} />
      <span className={styles.brain_name}>{item.label}</span>
    </span>
  );
};
