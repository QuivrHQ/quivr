import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { Brain } from "../context/BrainProvider/types";

export const createBrainFromBackend = async (
  axiosInstance: AxiosInstance,
  name: string
): Promise<Brain | undefined> => {
  try {
    const createdBrain = (await axiosInstance.post<Brain>(`/brains/`, { name }))
      .data;

    return createdBrain;
  } catch (error) {
    console.error(`Error creating brain ${name}`, error);
  }
};

export const getUserDefaultBrainFromBackend = async (
  axiosInstance: AxiosInstance
): Promise<Brain | undefined> => {
  try {
    const defaultBrain = (await axiosInstance.get<Brain>(`/brains/default/`))
      .data;

    return { id: defaultBrain.id, name: defaultBrain.name };
  } catch (error) {
    console.error(`Error getting user's default brain`, error);
  }
};

export const getBrainFromBE = async (
  axiosInstance: AxiosInstance,
  brainId: UUID
): Promise<Brain | undefined> => {
  try {
    const brain = (await axiosInstance.get<Brain>(`/brains/${brainId}/`)).data;

    return brain;
  } catch (error) {
    console.error(`Error getting brain ${brainId}`, error);

    throw new Error(`Error getting brain ${brainId}`);
  }
};

export const deleteBrainFromBE = async (
  axiosInstance: AxiosInstance,
  brainId: UUID
): Promise<void> => {
  try {
    (await axiosInstance.delete(`/brain/${brainId}/`)).data;
  } catch (error) {
    console.error(`Error deleting brain ${brainId}`, error);

    throw new Error(`Error deleting brain ${brainId}`);
  }
};

export const getAllUserBrainsFromBE = async (
  axiosInstance: AxiosInstance
): Promise<Brain[] | undefined> => {
  try {
    const brains = (await axiosInstance.get<{ brains: Brain[] }>(`/brains/`))
      .data;

    console.log("BRAINS", brains);

    return brains.brains;
  } catch (error) {
    console.error(`Error getting brain  for current user}`, error);

    throw new Error(`Error getting brain  for current user`);
  }
};
