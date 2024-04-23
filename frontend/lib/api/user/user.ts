import { Session } from "@supabase/auth-helpers-nextjs";
import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { UserStats } from "@/lib/types/User";

export enum CompanySize {
  One = "1-10",
  Two = "10-25",
  Three = "25-50",
  Four = "50-100",
  Five = "100-500",
  Six = "500-1000",
  Seven = "1000-5000",
  Eight = "+5000",
}

export enum UsagePurpose {
  Business = "Business",
  NGO = "NGO",
  Personal = "Personal",
  Student = "Student",
  Teacher = "Teacher",
}

export type UserIdentityUpdatableProperties = {
  username: string;
  company?: string;
  onboarded: boolean;
  company_size?: CompanySize;
  usage_purpose?: UsagePurpose;
};

export type UserIdentity = {
  id: UUID;
  onboarded: boolean;
  username: string;
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

export const getUser = async (
  axiosInstance: AxiosInstance
): Promise<UserStats> => (await axiosInstance.get<UserStats>("/user")).data;

export const deleteUser = async (
  axiosInstance: AxiosInstance,
  userId: string,
  session: Session
): Promise<void> => {
  if (session.user.id === userId) {
    await axiosInstance.delete(`/user/${userId}`);
  }
};
