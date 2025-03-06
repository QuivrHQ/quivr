import { AxiosInstance } from 'axios';
import { UUID } from 'crypto';

import { UserStats } from '@/lib/types/User';

export enum CompanySize {
  One = '1-10',
  Two = '10-25',
  Three = '25-50',
  Four = '50-100',
  Five = '100-250',
  Six = '250-500',
  Seven = '500-1000',
  Eight = '1000-5000',
  Nine = '+5000',
}

export enum UsagePurpose {
  Business = 'Business',
  NGO = 'NGO',
  Personal = 'Personal',
  Student = 'Student',
  Teacher = 'Teacher',
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
  email?: string;
  brains?: string[];
  brain_names?: string[];
  last_sign_in_at?: string;
};

export type CreateUserRequest = {
  firstName: string;
  lastName: string;
  email: string;
  brains: string[];
};

export type UpdateUserRequest = {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  brains: string[];
};

export type CreateUserResponse = {
  id: string;
  email: string;
  username: string;
};

export type UpdateUserResponse = {
  id: string;
  email: string;
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

export const getAllUsers = async (
  axiosInstance: AxiosInstance
): Promise<UserIdentity[]> => {
  const { data } = await axiosInstance.get<UserIdentity[]>(`/users`);

  return data;
};

export const createUser = async (
  userData: CreateUserRequest,
  axiosInstance: AxiosInstance
): Promise<CreateUserResponse> => {
  const response = await axiosInstance.post('/user/create', userData);

  // eslint-disable-next-line @typescript-eslint/no-unsafe-return
  return response.data;
};

export const updateUser = async (
  userData: UpdateUserRequest,
  axiosInstance: AxiosInstance
): Promise<UpdateUserResponse> => {
  const response = await axiosInstance.put('/user/update', userData);

  // eslint-disable-next-line @typescript-eslint/no-unsafe-return
  return response.data;
};

export const getUser = async (
  axiosInstance: AxiosInstance
): Promise<UserStats> => (await axiosInstance.get<UserStats>('/user')).data;

export const deleteUserData = async (
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.delete(`/user_data`);
};

export const getUserCredits = async (
  axiosInstance: AxiosInstance
): Promise<number> => (await axiosInstance.get<number>('/user/credits')).data;
