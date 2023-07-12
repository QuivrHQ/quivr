/* eslint-disable max-lines */
import { useState } from "react";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useToast } from "@/lib/hooks";

import { BrainRoleAssignation } from "../../../types";
import { generateBrainAssignation } from "../utils/generateBrainAssignation";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useShareBrain = (brainId: string) => {
  const baseUrl = window.location.origin;
  const { publish } = useToast();
  const { addBrainSubscriptions } = useBrainApi();
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);

  const brainShareLink = `${baseUrl}/brain_subscription_invitation=${brainId}`;
  const [sendingInvitation, setSendingInvitation] = useState(false);
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

  const inviteUsers = async (): Promise<void> => {
    setSendingInvitation(true);
    try {
      const inviteUsersPayload = roleAssignations
        .filter(({ email }) => email !== "")
        .map((assignation) => ({
          email: assignation.email,
          rights: assignation.role,
        }));

      await addBrainSubscriptions(brainId, inviteUsersPayload);

      publish({
        variant: "success",
        text: "Users successfully invited",
      });

      setIsShareModalOpen(false);
    } catch (error) {
      publish({
        variant: "danger",
        text: "An error occurred while sending invitations",
      });
    } finally {
      setSendingInvitation(false);
    }
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
    sendingInvitation,
    setIsShareModalOpen,
    isShareModalOpen,
  };
};
