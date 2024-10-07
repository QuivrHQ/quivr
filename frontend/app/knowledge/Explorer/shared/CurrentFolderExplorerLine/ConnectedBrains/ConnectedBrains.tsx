import { Brain } from "@/lib/context/BrainProvider/types";

import styles from "./ConnectedBrains.module.scss";

interface ConnectedbrainsProps {
  connectedBrains: Brain[];
}

const ConnectedBrains = ({
  connectedBrains,
}: ConnectedbrainsProps): JSX.Element => {
  return <div className={styles.main_container}>{connectedBrains.length}</div>;
};

export default ConnectedBrains;
