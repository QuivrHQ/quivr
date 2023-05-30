import { useSupabase } from "@/app/supabase-provider";
import axios from "axios";
export const useAxios = () => {
  const { session } = useSupabase();

  const axiosInstance = axios.create({
    baseURL: `${process.env.NEXT_PUBLIC_BACKEND_URL}`,
  });

  axiosInstance.interceptors.request.use(
    async (config) => {
      config.headers["Authorization"] = "Bearer " + session?.access_token;

      return config;
    },
    (error) => {
      console.error({ error });
      void Promise.reject(error);
    }
  );

  return {
    axiosInstance,
  };
};
