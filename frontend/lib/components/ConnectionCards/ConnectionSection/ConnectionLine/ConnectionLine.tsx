import { useState } from "react";

import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { useSync } from "@/lib/api/sync/useSync";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./ConnectionLine.module.scss";

interface ConnectionLineProps {
  label: string;
  index: number;
  id: number;
  warnUserOnDelete?: boolean;
}

export const ConnectionLine = ({
  label,
  index,
  id,
  warnUserOnDelete,
}: ConnectionLineProps): JSX.Element => {
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteModalOpened, setDeleteModalOpened] = useState(false);

  const { deleteUserSync } = useSync();
  const { setHasToReload } = useFromConnectionsContext();

  return (
    <>
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
              if (warnUserOnDelete) {
                setDeleteModalOpened(true);
              } else {
                await deleteUserSync(id);
                setHasToReload(true);
              }
            }}
          />
        </div>
      </div>
      <Modal
        isOpen={deleteModalOpened}
        setOpen={setDeleteModalOpened}
        size="auto"
        Trigger={<div />}
        CloseTrigger={<div />}
      >
        <div className={styles.modal_wrapper}>
          <div className={styles.modal_title}>
            <div className={styles.icon}>
              <Icon name="warning" size="large" color="warning" />
            </div>
            <span>
              It takes up to 24 hours to delete this connection. Are you sure
              you want to proceed?
            </span>
          </div>
          <div className={styles.buttons_wrapper}>
            <QuivrButton
              iconName="chevronLeft"
              label="Cancel"
              color="primary"
              onClick={() => setDeleteModalOpened(false)}
            />
            <QuivrButton
              iconName="delete"
              label="Delete"
              color="dangerous"
              isLoading={deleteLoading}
              onClick={async () => {
                setDeleteLoading(true);
                await deleteUserSync(id);
                setDeleteLoading(false);
                setHasToReload(true);
                setDeleteModalOpened(false);
              }}
            />
          </div>
        </div>
      </Modal>
    </>
  );
};
