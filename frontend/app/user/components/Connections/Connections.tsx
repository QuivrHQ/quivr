import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";

import styles from "./Connections.module.scss";

export const Connections = (): JSX.Element => {
  return (
    <div className={styles.connections_wrapper}>
      <span className={styles.title}>Link apps you want to search across</span>
      <ConnectionCards />
    </div>
  );
};
