import { AxiosInstance } from "axios";

import { Onboarding } from "@/lib/types/Onboarding";

export const getOnboarding = async (
  axiosInstance: AxiosInstance
): Promise<Onboarding> => {
  return (await axiosInstance.get<Onboarding>("/onboarding")).data;
};

export const updateOnboarding = async (
  onboarding: Partial<Onboarding>,
  axiosInstance: AxiosInstance
): Promise<Onboarding> => {
  return (await axiosInstance.put<Onboarding>("/onboarding", onboarding)).data;
};
