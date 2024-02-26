"use client";

import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { ButtonType } from "@/lib/types/QuivrButton";

import { BrainManagementTabs } from "./BrainManagementTabs/BrainManagementTabs";
import { DeleteOrUnsubscribeConfirmationModal } from "./BrainManagementTabs/components/DeleteOrUnsubscribeModal/DeleteOrUnsubscribeConfirmationModal";
import { useBrainManagementTabs } from "./BrainManagementTabs/hooks/useBrainManagementTabs";
import { getBrainPermissions } from "./BrainManagementTabs/utils/getBrainPermissions";
import { useBrainManagement } from "./hooks/useBrainManagement";
import styles from "./page.module.scss";

const BrainsManagement = (): JSX.Element => {
  const { brain } = useBrainManagement();
  const {
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    isDeleteOrUnsubscribeRequestPending,
  } = useBrainManagementTabs(brain?.id);
  const { allBrains } = useBrainContext();
  const { isOwnedByCurrentUser } = getBrainPermissions({
    brainId: brain?.id,
    userAccessibleBrains: allBrains,
  });

  const buttons: ButtonType[] = [
    {
      label: "Delete brain",
      color: "dangerous",
      onClick: () => {
        setIsDeleteOrUnsubscribeModalOpened(true);
      },
      iconName: "brain",
    },
  ];

  if (!brain) {
    return <></>;
  }

  return (
    <>
      <div className={styles.brain_management_wrapper}>
        <PageHeader iconName="brain" label={brain.name} buttons={buttons} />
        <div className={styles.content_wrapper}>
          <BrainManagementTabs />
        </div>
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
    </>
  );
};

export default BrainsManagement;
