import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import { BrainItem } from "./BrainItem/BrainItem";
import styles from "./BrainsList.module.scss";

type BrainsListProps = {
  brains: MinimalBrainForUser[];
};

export const BrainsList = ({ brains }: BrainsListProps): JSX.Element => {
  return (
    <div className={styles.brains_wrapper}>
      <div className={styles.columns}>
        <span className={styles.name}>Name</span>
        <span className={styles.description}>Description</span>
      </div>
      {brains.map((brain, index) => (
        <div key={brain.id}>
          <BrainItem brain={brain} even={!(index % 2)} />
        </div>
      ))}
    </div>
  );
};
