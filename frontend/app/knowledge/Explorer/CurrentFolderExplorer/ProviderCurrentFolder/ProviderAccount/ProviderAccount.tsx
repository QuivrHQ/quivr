import { Sync } from "@/lib/api/sync/types";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./ProviderAccount.module.scss";

interface ProviderAccountProps {
  sync: Sync;
  index: number;
}

const ProviderAccount = ({
  sync,
  index,
}: ProviderAccountProps): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <div className={styles.left}>
        <ConnectionIcon letter={sync.email[0]} index={index} />
        <span className={styles.name}>{sync.email}</span>
      </div>
      <Icon
        name="chevronRight"
        size="normal"
        color="black"
        handleHover={true}
      />
    </div>
  );
};

export default ProviderAccount;
