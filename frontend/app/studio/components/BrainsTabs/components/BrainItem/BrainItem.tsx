import Link from "next/link";

import Icon from "@/lib/components/ui/Icon/Icon";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import styles from "./BrainItem.module.scss";

type BrainItemProps = {
  brain: MinimalBrainForUser;
  even: boolean;
};

export const BrainItem = ({ brain, even }: BrainItemProps): JSX.Element => {
  return (
    <div
      className={`
      ${even ? styles.even : styles.odd}
      ${styles.brain_item_wrapper}
      `}
    >
      <Link className={styles.brain_info_wrapper} href={`/studio/${brain.id}`}>
        <span className={styles.name}>{brain.name}</span>
        <span className={styles.description}>{brain.description}</span>
      </Link>
      <Icon name="delete" size="normal" color="dangerous" handleHover={true} />
    </div>
  );
};
