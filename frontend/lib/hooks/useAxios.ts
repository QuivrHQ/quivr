import axios, {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { DEFAULT_BACKEND_URL } from "../config/CONSTANTS";

const axiosInstance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_BACKEND_URL ?? DEFAULT_BACKEND_URL}`,
});

export const useAxios = (): { axiosInstance: AxiosInstance } => {
  let { session } = useSupabase();
  const { supabase } = useSupabase();

  axiosInstance.interceptors.request.clear();
  axiosInstance.interceptors.request.use(
    async (value: InternalAxiosRequestConfig) => {
      // Check if the session is valid
      if (session?.expires_at && session.expires_at * 1000 < Date.now()) {
        // If the session is not valid, refresh it
        const { data, error } = await supabase.auth.refreshSession();
        if (error) {
          throw error;
        }
        session = data.session;
      }

      value.headers["Authorization"] = `Bearer ${session?.access_token ?? ""}`;

      return value;
    },
    (error: AxiosError) => {
      console.error({ error });

      return Promise.reject(error);
    }
  );

  return {
    axiosInstance,
  };
};
