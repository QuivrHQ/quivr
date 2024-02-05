import Link from "next/link";

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
  const {
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    isDeleteOrUnsubscribeRequestPending,
  } = useBrainManagementTabs();

  const { allBrains } = useBrainContext();

  const { isOwnedByCurrentUser } = getBrainPermissions({
    brainId: brain.id,
    userAccessibleBrains: allBrains,
  });

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
      <Icon
        name="delete"
        size="normal"
        color="dangerous"
        handleHover={true}
        onClick={() => setIsDeleteOrUnsubscribeModalOpened(true)}
      />
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
