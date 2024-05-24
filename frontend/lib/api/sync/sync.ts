import { AxiosInstance } from "axios";

export const syncGoogleDrive = async (
  name: string,
  axiosInstance: AxiosInstance
): Promise<{ authorization_url: string }> => {
  const connection = (
    await axiosInstance.post<{ authorization_url: string }>(
      `/sync/google/authorize?name=${name}`
    )
  ).data;

  return connection;
};

export const syncSharepoint = async (
  name: string,
  axiosInstance: AxiosInstance
): Promise<{ authorization_url: string }> => {
  const connection = (
    await axiosInstance.post<{ authorization_url: string }>(
      `/sync/azure/authorize?name=${name}`
    )
  ).data;

  return connection;
};
