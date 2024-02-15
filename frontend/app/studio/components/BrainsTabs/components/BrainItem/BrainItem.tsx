import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { DeleteOrUnsubscribeConfirmationModal } from "@/app/studio/[brainId]/components/BrainManagementTabs/components/Modals/DeleteOrUnsubscribeConfirmationModal";
import { useBrainManagementTabs } from "@/app/studio/[brainId]/components/BrainManagementTabs/hooks/useBrainManagementTabs";
import { getBrainPermissions } from "@/app/studio/[brainId]/components/BrainManagementTabs/utils/getBrainPermissions";
import Icon from "@/lib/components/ui/Icon/Icon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import styles from "./BrainItem.module.scss";

type BrainItemProps = {
  brain: MinimalBrainForUser;
  even: boolean;
};

export const BrainItem = ({ brain, even }: BrainItemProps): JSX.Element => {
  const [optionsOpened, setOptionsOpened] = useState<boolean>(false);
  const [deleteHovered, setDeleteHovered] = useState<boolean>(false);
  const [editHovered, setEditHovered] = useState<boolean>(false);
  const {
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    isDeleteOrUnsubscribeRequestPending,
  } = useBrainManagementTabs(brain.id);

  const { allBrains } = useBrainContext();

  const { isOwnedByCurrentUser } = getBrainPermissions({
    brainId: brain.id,
    userAccessibleBrains: allBrains,
  });

  const optionsRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        optionsRef.current &&
        !optionsRef.current.contains(event.target as Node)
      ) {
        setOptionsOpened(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

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

      <div>
        <div
          onClick={(event: React.MouseEvent<HTMLElement>) => {
            event.stopPropagation();
            setOptionsOpened(!optionsOpened);
          }}
        >
          <Icon name="options" size="normal" color="black" handleHover={true} />
        </div>
        {optionsOpened && (
          <div className={styles.options_menu} ref={optionsRef}>
            <div
              className={styles.option}
              onClick={() => setIsDeleteOrUnsubscribeModalOpened(true)}
              onMouseEnter={() => setDeleteHovered(true)}
              onMouseLeave={() => setDeleteHovered(false)}
            >
              <span>Delete</span>
              <Icon
                name="delete"
                size="normal"
                color="dangerous"
                hovered={deleteHovered}
              />
            </div>
            <div
              className={styles.option}
              onClick={() => (window.location.href = `/studio/${brain.id}`)}
              onMouseEnter={() => setEditHovered(true)}
              onMouseLeave={() => setEditHovered(false)}
            >
              <span>Edit</span>
              <Icon
                name="edit"
                size="normal"
                color="black"
                hovered={editHovered}
              />
            </div>
          </div>
        )}
      </div>
      <DeleteOrUnsubscribeConfirmationModal
        isOpen={isDeleteOrUnsubscribeModalOpened}
        setOpen={setIsDeleteOrUnsubscribeModalOpened}
        onConfirm={() => void handleUnsubscribeOrDeleteBrain()}
        isOwnedByCurrentUser={isOwnedByCurrentUser}
        isDeleteOrUnsubscribeRequestPending={
          isDeleteOrUnsubscribeRequestPending
        }
      />
    </div>
  );
};
