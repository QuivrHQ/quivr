import { useState } from "react";

import { useToast } from "@/lib/hooks";

import { BrainRoleAssignation } from "../../../types";
import { generateBrainAssignation } from "../utils/generateBrainAssignation";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useShareBrain = (brainId: string) => {
  const baseUrl = window.location.origin;
  const { publish } = useToast();

  const brainShareLink = `${baseUrl}/brain_subscription_invitation=${brainId}`;

  const [roleAssignations, setRoleAssignation] = useState<
    BrainRoleAssignation[]
  >([generateBrainAssignation()]);

  const handleCopyInvitationLink = async () => {
    await navigator.clipboard.writeText(brainShareLink);
    publish({
      variant: "success",
      text: "Copied to clipboard",
    });
  };

  const removeRoleAssignation = (assignationIndex: number) => () => {
    if (roleAssignations.length === 1) {
      return;
    }
    setRoleAssignation(
      roleAssignations.filter((_, index) => index !== assignationIndex)
    );
  };

  const updateRoleAssignation =
    (rowIndex: number) => (data: BrainRoleAssignation) => {
      const concernedRow = roleAssignations[rowIndex];

      if (concernedRow !== undefined) {
        setRoleAssignation(
          roleAssignations.map((row, index) => {
            if (index === rowIndex) {
              return data;
            }

            return row;
          })
        );
      } else {
        setRoleAssignation([...roleAssignations, data]);
      }
    };

  const inviteUsers = (): void => {
    const inviteUsersPayload = roleAssignations
      .filter(({ email }) => email !== "")
      .map((assignation) => ({
        email: assignation.email,
        role: assignation.role,
      }));

    alert(
      `You will soon be able to invite ${JSON.stringify(
        inviteUsersPayload
      )}. Wait a bit`
    );
  };

  const addNewRoleAssignationRole = () => {
    setRoleAssignation([...roleAssignations, generateBrainAssignation()]);
  };

  return {
    roleAssignations,
    brainShareLink,
    handleCopyInvitationLink,
    updateRoleAssignation,
    removeRoleAssignation,
    inviteUsers,
    addNewRoleAssignationRole,
  };
};
