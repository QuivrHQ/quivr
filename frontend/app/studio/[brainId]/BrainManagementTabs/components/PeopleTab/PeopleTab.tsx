"use client";

import { UUID } from "crypto";
import { ImUserPlus } from "react-icons/im";

import { BrainUsers } from "@/lib/components/BrainUsers/BrainUsers";
import { UserToInvite } from "@/lib/components/UserToInvite";
import Button from "@/lib/components/ui/Button";
import { useShareBrain } from "@/lib/hooks/useShareBrain";

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
    <>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void inviteUsers();
        }}
      >
        <div>
          <div />
          <p>Invite new users</p>

          {roleAssignations.map((roleAssignation, index) => (
            <UserToInvite
              key={roleAssignation.id}
              onChange={updateRoleAssignation(index)}
              removeCurrentInvitation={removeRoleAssignation(index)}
              roleAssignation={roleAssignation}
            />
          ))}
          <Button
            onClick={addNewRoleAssignationRole}
            disabled={sendingInvitation || !canAddNewRow}
          >
            <ImUserPlus />
          </Button>
        </div>

        <div>
          <Button
            isLoading={sendingInvitation}
            disabled={roleAssignations.length === 0}
            type="submit"
          >
            Share
          </Button>
        </div>
      </form>
      <div />
      <p>Users with access</p>
      <BrainUsers brainId={brainId} />
    </>
  );
};
