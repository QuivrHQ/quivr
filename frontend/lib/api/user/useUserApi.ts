import { useAxios } from '@/lib/hooks';

import {
  createUser,
  CreateUserRequest,
  CreateUserResponse,
  deleteUserData,
  getAllUsers,
  getUser,
  getUserCredits,
  getUserIdentity,
  updateUser,
  updateUserIdentity,
  UpdateUserRequest,
  UpdateUserResponse,
  UserIdentity,
  UserIdentityUpdatableProperties,
} from './user';

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useUserApi = () => {
  const { axiosInstance } = useAxios();

  return {
    createUser: async (
      userData: CreateUserRequest
    ): Promise<CreateUserResponse> => createUser(userData, axiosInstance),
    updateUser: async (
      userData: UpdateUserRequest
    ): Promise<UpdateUserResponse> => updateUser(userData, axiosInstance),
    updateUserIdentity: async (
      userIdentityUpdatableProperties: UserIdentityUpdatableProperties
    ) => updateUserIdentity(userIdentityUpdatableProperties, axiosInstance),
    getUserIdentity: async () => getUserIdentity(axiosInstance),
    getAllUsers: async (): Promise<UserIdentity[]> =>
      getAllUsers(axiosInstance),
    getUser: async () => getUser(axiosInstance),
    deleteUserData: async () => deleteUserData(axiosInstance),
    getUserCredits: async () => getUserCredits(axiosInstance),
  };
};
