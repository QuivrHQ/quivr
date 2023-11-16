import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { BrainRoleType } from "@/lib/components/BrainUsers/types";

export const acceptInvitation = async (
  brainId: UUID,
  axiosInstance: AxiosInstance
): Promise<{ message: string }> => {
  const acceptedInvitation = (
    await axiosInstance.post<{ message: string }>(
      `/brains/${brainId}/subscription/accept`
    )
  ).data;

  return acceptedInvitation;
};

export const declineInvitation = async (
  brainId: UUID,
  axiosInstance: AxiosInstance
): Promise<{ message: string }> => {
  const deletedInvitation = (
    await axiosInstance.post<{ message: string }>(
      `/brains/${brainId}/subscription/decline`
    )
  ).data;

  return deletedInvitation;
};

export type InvitationBrain = {
  name: string;
  role: BrainRoleType;
};

//TODO: rename rights to role in Backend and use InvitationBrain instead of BackendInvitationBrain
type BackendInvitationBrain = Omit<InvitationBrain, "role"> & {
  rights: BrainRoleType;
};

export const getInvitation = async (
  brainId: UUID,
  axiosInstance: AxiosInstance
): Promise<InvitationBrain> => {
  const invitation = (
    await axiosInstance.get<BackendInvitationBrain>(
      `/brains/${brainId}/subscription`
    )
  ).data;

  return {
    name: invitation.name,
    role: invitation.rights,
  };
};
type ApiBrainSecrets = Record<string, string>;

export const subscribeToBrain = async (
  brainId: UUID,
  axiosInstance: AxiosInstance,
  secrets?: ApiBrainSecrets
): Promise<{ message: string }> => {
  const subscribedToBrain = (
    await axiosInstance.post<{ message: string }>(
      `/brains/${brainId}/subscribe`,
      secrets
    )
  ).data;

  return subscribedToBrain;
};

export const unsubscribeFromBrain = async (
  brainId: UUID,
  axiosInstance: AxiosInstance
): Promise<{ message: string }> =>
  (
    await axiosInstance.post<{ message: string }>(
      `/brains/${brainId}/unsubscribe`
    )
  ).data;
