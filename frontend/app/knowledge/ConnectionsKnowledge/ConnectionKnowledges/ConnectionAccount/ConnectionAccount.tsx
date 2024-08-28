import { Sync } from "@/lib/api/sync/types";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./ConnectionAccount.module.scss";

interface ConnectionAccountProps {
  sync: Sync;
  index: number;
}

const ConnectionAccount = ({
  sync,
  index,
}: ConnectionAccountProps): JSX.Element => {
  return (
    <div className={styles.account_line_wrapper}>
      <Icon
        name="chevronRight"
        size="normal"
        color="black"
        handleHover={true}
      />
      <ConnectionIcon letter={sync.email[0]} index={index} />
      <span>{sync.email}</span>
    </div>
  );
};

export default ConnectionAccount;
