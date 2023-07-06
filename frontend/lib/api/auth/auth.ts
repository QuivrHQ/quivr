import { AxiosInstance } from "axios";

export const createApiKey = async (
  axiosInstance: AxiosInstance
): Promise<string> => {
  const response = await axiosInstance.post<{ api_key: string }>("/api-key");

  return response.data.api_key;
};
