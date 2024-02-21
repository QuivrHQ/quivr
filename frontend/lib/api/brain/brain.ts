/* eslint-disable max-lines */
import { AxiosInstance } from "axios";

import { BrainRoleType } from "@/lib/components/BrainUsers/types";
import {
  BackendMinimalBrainForUser,
  Brain,
  MinimalBrainForUser,
  PublicBrain,
} from "@/lib/context/BrainProvider/types";

import {
  CreateBrainInput,
  IntegrationBrains,
  ListFilesProps,
  SubscriptionUpdatableProperties,
  UpdateBrainInput,
} from "./types";
import { mapBackendMinimalBrainToMinimalBrain } from "./utils/mapBackendMinimalBrainToMinimalBrain";
import {
  BackendSubscription,
  mapSubscriptionToBackendSubscription,
} from "./utils/mapSubscriptionToBackendSubscription";
import { mapSubscriptionUpdatablePropertiesToBackendSubscriptionUpdatableProperties } from "./utils/mapSubscriptionUpdatablePropertiesToBackendSubscriptionUpdatableProperties";

export const createBrain = async (
  brain: CreateBrainInput,
  axiosInstance: AxiosInstance
): Promise<MinimalBrainForUser> => {
  return mapBackendMinimalBrainToMinimalBrain(
    (await axiosInstance.post<BackendMinimalBrainForUser>(`/brains/`, brain))
      .data
  );
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
  return mapBackendMinimalBrainToMinimalBrain(
    (await axiosInstance.get<BackendMinimalBrainForUser>(`/brains/default/`))
      .data
  );
};

export const getBrains = async (
  axiosInstance: AxiosInstance
): Promise<MinimalBrainForUser[]> => {
  const { brains } = (
    await axiosInstance.get<{ brains: BackendMinimalBrainForUser[] }>(
      `/brains/`
    )
  ).data;

  return brains.map(mapBackendMinimalBrainToMinimalBrain);
};

export type Subscription = { email: string; role: BrainRoleType };

export const addBrainSubscriptions = async (
  brainId: string,
  subscriptions: Subscription[],
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.post(
    `/brains/${brainId}/subscription`,
    subscriptions.map(mapSubscriptionToBackendSubscription)
  );
};

export const getBrainUsers = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<Subscription[]> => {
  const brainsUsers = (
    await axiosInstance.get<BackendSubscription[]>(`/brains/${brainId}/users`)
  ).data;

  return brainsUsers.map((brainUser) => ({
    email: brainUser.email,
    role: brainUser.rights,
  }));
};

export const updateBrainAccess = async (
  brainId: string,
  userEmail: string,
  subscription: SubscriptionUpdatableProperties,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.put(`/brains/${brainId}/subscription`, {
    ...mapSubscriptionUpdatablePropertiesToBackendSubscriptionUpdatableProperties(
      subscription
    ),
    email: userEmail,
  });
};

export const setAsDefaultBrain = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.post(`/brains/${brainId}/default`);
};

export const updateBrain = async (
  brainId: string,
  brain: UpdateBrainInput,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.put(`/brains/${brainId}/`, brain);
};

export const getPublicBrains = async (
  axiosInstance: AxiosInstance
): Promise<PublicBrain[]> => {
  return (await axiosInstance.get<PublicBrain[]>(`/brains/public`)).data;
};

export const updateBrainSecrets = async (
  brainId: string,
  secrets: Record<string, string>,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.put(`/brains/${brainId}/secrets-values`, secrets);
};

export const getDocsFromQuestion = async (
  brainId: string,
  question: string,
  axiosInstance: AxiosInstance
): Promise<ListFilesProps["files"]> => {
  return (
    await axiosInstance.post<Record<"docs", ListFilesProps["files"]>>(
      `/brains/${brainId}/documents`,
      {
        question,
      }
    )
  ).data.docs;
};

export const getIntegrationBrains = async (
  axiosInstance: AxiosInstance
): Promise<IntegrationBrains[]> => {
  return (await axiosInstance.get<IntegrationBrains[]>(`/brains/integrations/`))
    .data;
};
