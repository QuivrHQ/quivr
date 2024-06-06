import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { useSync } from "@/lib/api/sync/useSync";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./ConnectionLine.module.scss";

interface ConnectionLineProps {
  label: string;
  index: number;
  id: number;
}

export const ConnectionLine = ({
  label,
  index,
  id,
}: ConnectionLineProps): JSX.Element => {
  const { deleteUserSync } = useSync();
  const { setHasToReload } = useFromConnectionsContext();

  return (
    <div className={styles.connection_line_wrapper}>
      <div className={styles.left}>
        <ConnectionIcon letter={label[0]} index={index} />
        <span className={styles.label}>{label}</span>
      </div>
      <div className={styles.icons}>
        <Icon
          name="delete"
          size="normal"
          color="dangerous"
          handleHover={true}
          onClick={async () => {
            await deleteUserSync(id);
            setHasToReload(true);
          }}
        />
      </div>
    </div>
  );
};
