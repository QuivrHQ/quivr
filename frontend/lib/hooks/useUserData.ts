import { useQuery } from "@tanstack/react-query";

import { USER_DATA_KEY, USER_IDENTITY_DATA_KEY } from "../api/user/config";
import { useUserApi } from "../api/user/useUserApi";
import { UserIdentity } from "../api/user/user";
import { UserStats } from "../types/User";

type UseUserDataProps = {
  userData: UserStats | undefined;
  userIdentityData: UserIdentity | undefined;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useUserData = (): UseUserDataProps => {
  const { getUser } = useUserApi();
  const { getUserIdentity } = useUserApi();

  const { data: userData } = useQuery({
    queryKey: [USER_DATA_KEY],
    queryFn: getUser,
  });

  const { data: userIdentityData } = useQuery({
    queryKey: [USER_IDENTITY_DATA_KEY],
    queryFn: getUserIdentity,
  });

  return {
    userData,
    userIdentityData,
  };
};
