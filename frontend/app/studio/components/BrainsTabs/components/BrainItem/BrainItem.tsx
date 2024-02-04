import Link from "next/link";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import styles from "./BrainItem.module.scss";

type BrainItemProps = {
  brain: MinimalBrainForUser;
  even: boolean;
};

export const BrainItem = ({ brain }: BrainItemProps): JSX.Element => {
  return (
    <div className={styles.brain_item_wrapper}>
      <Link href={`/studio/${brain.id}`}>
        <div className={styles.brain_info_wrapper}>
          <span className={styles.name}>{brain.name}</span>
          <span className={styles.description}>{brain.description}</span>
        </div>
      </Link>
    </div>
  );
};
