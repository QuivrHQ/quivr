import axios, { AxiosError, AxiosInstance } from "axios";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { DEFAULT_BACKEND_URL } from "../config/CONSTANTS";

const axiosInstance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_BACKEND_URL ?? DEFAULT_BACKEND_URL}`,
});

export const useAxios = (): { axiosInstance: AxiosInstance } => {
  const { session } = useSupabase();
  axiosInstance.interceptors.request.clear();
  axiosInstance.interceptors.request.use(
    (config) => {
      config.headers["Authorization"] = `Bearer ${session?.access_token ?? ""}`;

      return config;
    },
    (error: AxiosError) => {
      console.error({ error });
      void Promise.reject(error);
    }
  );

  return {
    axiosInstance,
  };
};
