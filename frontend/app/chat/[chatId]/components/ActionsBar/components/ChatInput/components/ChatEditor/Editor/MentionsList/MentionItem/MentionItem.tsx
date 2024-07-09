import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./MentionItem.module.scss";

import { SuggestionDataType, SuggestionItem } from "../../types";

type MentionItemProps = {
  item: SuggestionItem;
  type: SuggestionDataType;
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
      <Icon name="brain" size="normal" color={"black"} />
      <span className={styles.brain_name}>{item.label}</span>
    </span>
  );
};
