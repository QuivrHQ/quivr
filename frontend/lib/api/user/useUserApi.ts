import { useAxios } from '@/lib/hooks';

import {
  createUser,
  CreateUserRequest,
  CreateUserResponse,
  deleteUserData,
  getUser,
  getUserCredits,
  getUserIdentity,
  updateUserIdentity,
  UserIdentityUpdatableProperties,
} from './user';

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useUserApi = () => {
  const { axiosInstance } = useAxios();

  return {
    createUser: async (
      userData: CreateUserRequest
    ): Promise<CreateUserResponse> => createUser(userData, axiosInstance),
    updateUserIdentity: async (
      userIdentityUpdatableProperties: UserIdentityUpdatableProperties
    ) => updateUserIdentity(userIdentityUpdatableProperties, axiosInstance),
    getUserIdentity: async () => getUserIdentity(axiosInstance),
    getUser: async () => getUser(axiosInstance),
    deleteUserData: async () => deleteUserData(axiosInstance),
    getUserCredits: async () => getUserCredits(axiosInstance),
  };
};
