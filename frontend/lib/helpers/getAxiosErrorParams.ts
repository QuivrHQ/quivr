import { AxiosResponse, isAxiosError } from "axios";

type AxiosErrorParams = {
  message: string;
  status: number;
};
export const getAxiosErrorParams = (
  e: unknown
): AxiosErrorParams | undefined => {
  if (isAxiosError(e) && e.response?.data !== undefined) {
    return {
      message: (
        e.response as AxiosResponse<{
          detail: string;
        }>
      ).data.detail,
      status: e.response.status,
    };
  }

  return undefined;
};
