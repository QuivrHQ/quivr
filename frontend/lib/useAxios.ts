import { useSupabase } from "@/app/supabase-provider";
import axios from "axios";
import { useBrainConfig } from "./context/BrainConfigProvider/hooks/useBrainConfig";

const axiosInstance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_BACKEND_URL}`,
});

export const useAxios = () => {
  const { session } = useSupabase();
  const {
    config: { backendUrl },
  } = useBrainConfig();
  axiosInstance.interceptors.request.clear();
  axiosInstance.interceptors.request.use(
    async (config) => {
      config.headers["Authorization"] = "Bearer " + session?.access_token;
      config.baseURL = backendUrl ?? config.baseURL;

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
