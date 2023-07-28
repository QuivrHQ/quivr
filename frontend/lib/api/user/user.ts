import { AxiosInstance } from "axios";
import { UUID } from "crypto";

export type UserIdentityUpdatableProperties = {
  openai_api_key?: string | null;
};

export type UserIdentity = {
  openai_api_key?: string | null;
  user_id: UUID;
};

export const updateUserIdentity = async (
  userUpdatableProperties: UserIdentityUpdatableProperties,
  axiosInstance: AxiosInstance
): Promise<UserIdentity> =>
  axiosInstance.put(`/user/identity`, userUpdatableProperties);

export const getUserIdentity = async (
  axiosInstance: AxiosInstance
): Promise<UserIdentity> => {
  const { data } = await axiosInstance.get<UserIdentity>(`/user/identity`);

  return data;
};
