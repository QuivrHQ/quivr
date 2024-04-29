import { Session } from "@supabase/supabase-js";

import { useAxios } from "@/lib/hooks";

import {
  deleteUser,
  getUser,
  getUserCredits,
  getUserIdentity,
  updateUserIdentity,
  UserIdentityUpdatableProperties,
} from "./user";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useUserApi = () => {
  const { axiosInstance } = useAxios();

  return {
    updateUserIdentity: async (
      userIdentityUpdatableProperties: UserIdentityUpdatableProperties
    ) => updateUserIdentity(userIdentityUpdatableProperties, axiosInstance),
    getUserIdentity: async () => getUserIdentity(axiosInstance),
    getUser: async () => getUser(axiosInstance),
    deleteUser: async (userId: string, session: Session) =>
      deleteUser(axiosInstance, userId, session),
    getUserCredits: async () => getUserCredits(axiosInstance),
  };
};
