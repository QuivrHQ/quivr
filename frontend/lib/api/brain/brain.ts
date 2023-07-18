import { AxiosInstance } from "axios";

import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import { Brain, MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { Document } from "@/lib/types/Document";

export const getBrainDocuments = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<Document[]> => {
  const response = await axiosInstance.get<{ documents: Document[] }>(
    `/explore/?brain_id=${brainId}`
  );

  return response.data.documents;
};

export const createBrain = async (
  name: string,
  axiosInstance: AxiosInstance
): Promise<MinimalBrainForUser> => {
  const createdBrain = (
    await axiosInstance.post<MinimalBrainForUser>(`/brains/`, { name })
  ).data;

  return createdBrain;
};

export const getBrain = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<Brain | undefined> => {
  const brain = (
    await axiosInstance.get<Brain | undefined>(`/brains/${brainId}/`)
  ).data;

  return brain;
};

export const deleteBrain = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.delete(`/brains/${brainId}/subscription`);
};

export const getDefaultBrain = async (
  axiosInstance: AxiosInstance
): Promise<MinimalBrainForUser | undefined> => {
  return (await axiosInstance.get<MinimalBrainForUser>(`/brains/default/`))
    .data;
};

export const getBrains = async (
  axiosInstance: AxiosInstance
): Promise<MinimalBrainForUser[]> => {
  const brains = (
    await axiosInstance.get<{ brains: MinimalBrainForUser[] }>(`/brains/`)
  ).data;

  return brains.brains;
};

export type Subscription = { email: string; rights: BrainRoleType };

export const addBrainSubscriptions = async (
  brainId: string,
  subscriptions: Subscription[],
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.post(`/brains/${brainId}/subscription`, subscriptions);
};

export const getBrainUsers = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<Subscription[]> => {
  return (await axiosInstance.get<Subscription[]>(`/brains/${brainId}/users`))
    .data;
};

export type SubscriptionUpdatableProperties = {
  rights: BrainRoleType | null;
};

export const updateBrainAccess = async (
  brainId: string,
  userEmail: string,
  subscription: SubscriptionUpdatableProperties,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.put(`/brains/${brainId}/subscription`, {
    ...subscription,
    email: userEmail,
  });
};
