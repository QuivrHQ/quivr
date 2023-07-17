import { AxiosInstance } from "axios";

import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import { Brain } from "@/lib/context/BrainProvider/types";
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
): Promise<Brain> => {
  const createdBrain = (await axiosInstance.post<Brain>(`/brains/`, { name }))
    .data;

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
  await axiosInstance.delete(`/brain/${brainId}/subscription`);
};

export const getDefaultBrain = async (
  axiosInstance: AxiosInstance
): Promise<Brain | undefined> => {
  const defaultBrain = (await axiosInstance.get<Brain>(`/brains/default/`))
    .data;

  return { id: defaultBrain.id, name: defaultBrain.name };
};

export const getBrains = async (
  axiosInstance: AxiosInstance
): Promise<Brain[]> => {
  const brains = (await axiosInstance.get<{ brains: Brain[] }>(`/brains/`))
    .data;

  return brains.brains;
};

export type Subscription = { email: string; rights: BrainRoleType }[];

export const addBrainSubscriptions = async (
  brainId: string,
  subscriptions: Subscription,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.post(`/brain/${brainId}/subscription`, subscriptions);
};
