"use client";

import { UUID } from "crypto";

import { BrainUsers } from "@/app/studio/[brainId]/BrainManagementTabs/components/PeopleTab/BrainUsers/BrainUsers";
import { UserToInvite } from "@/app/studio/[brainId]/BrainManagementTabs/components/PeopleTab/BrainUsers/components/UserToInvite/UserToInvite";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useShareBrain } from "@/lib/hooks/useShareBrain";

import styles from "./PeopleTab.module.scss";

type ShareBrainModalProps = {
  brainId: UUID;
};

export const PeopleTab = ({ brainId }: ShareBrainModalProps): JSX.Element => {
  const {
    roleAssignations,
    updateRoleAssignation,
    removeRoleAssignation,
    inviteUsers,
    addNewRoleAssignationRole,
    sendingInvitation,
    canAddNewRow,
  } = useShareBrain(brainId);

  return (
    <div className={styles.people_tab_wrapper}>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void inviteUsers();
        }}
      >
        <div className={styles.section_wrapper}>
          <span className={styles.section_title}>Invite new users</span>
          {roleAssignations.map((roleAssignation, index) => (
            <UserToInvite
              key={roleAssignation.id}
              onChange={updateRoleAssignation(index)}
              removeCurrentInvitation={removeRoleAssignation(index)}
              roleAssignation={roleAssignation}
            />
          ))}
          <div className={styles.buttons_wrapper}>
            <QuivrButton
              onClick={addNewRoleAssignationRole}
              disabled={sendingInvitation || !canAddNewRow}
              label="Add new user"
              color="primary"
              iconName="add"
            ></QuivrButton>
            <QuivrButton
              isLoading={sendingInvitation}
              disabled={roleAssignations.length === 0}
              label="Invite"
              color="primary"
              iconName="share"
              onClick={inviteUsers}
            ></QuivrButton>
          </div>
        </div>
      </form>
      <div className={`${styles.section_wrapper} ${styles.last}`}>
        <span className={styles.section_title}>Users with access</span>
        <BrainUsers brainId={brainId} />
      </div>
    </div>
  );
};
