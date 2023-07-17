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

export const checkValidInvitation = async (
  brainId: UUID,
  axiosInstance: AxiosInstance
): Promise<boolean> => {
  const answer = await axiosInstance.get<{ hasInvitation: boolean }>(
    `/brains/${brainId}/subscription`
  );
  const toto = answer.data["hasInvitation"];
  console.log(answer);

  return toto;
};
