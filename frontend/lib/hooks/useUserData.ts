import { useQuery } from "@tanstack/react-query";

import { USER_DATA_KEY } from "../api/user/config";
import { useUserApi } from "../api/user/useUserApi";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useUserData = () => {
  const { getUser } = useUserApi();

  const { data: userData } = useQuery({
    queryKey: [USER_DATA_KEY],
    queryFn: getUser,
  });

  return {
    userData,
  };
};
