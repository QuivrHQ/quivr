import { AxiosInstance } from "axios";
import { UUID } from "crypto";

export const acceptInvitation = async (
  brainId: UUID,
  axiosInstance: AxiosInstance
): Promise<{ message: string }> => {
  const acceptedInvitation = (
    await axiosInstance.post<{ message: string }>(
      `/brains/${brainId}/subscription/accept`
    )
  ).data;

  console.log("acceptedInvitation", acceptedInvitation);

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
};

export const getInvitation = async (
  brainId: UUID,
  axiosInstance: AxiosInstance
): Promise<InvitationBrain> => {
  return (
    await axiosInstance.get<InvitationBrain>(`/brains/${brainId}/subscription`)
  ).data;
};
