import { useEffect, useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { defaultBrainConfig } from "../config/defaultBrainConfig";

interface FetchInstance {
  get: (url: string, headers?: HeadersInit) => Promise<Response>;
  post: (
    url: string,
    body: BodyInit | null | undefined,
    headers?: HeadersInit
  ) => Promise<Response>;
  put: (
    url: string,
    body: BodyInit | null | undefined,
    headers?: HeadersInit
  ) => Promise<Response>;
  delete: (url: string, headers?: HeadersInit) => Promise<Response>;
}

const fetchInstance: FetchInstance = {
  get: async (url, headers) => fetch(url, { method: "GET", headers }),
  post: async (url, body, headers) =>
    fetch(url, { method: "POST", body, headers }),
  put: async (url, body, headers) =>
    fetch(url, { method: "PUT", body, headers }),
  delete: async (url, headers) => fetch(url, { method: "DELETE", headers }),
};

export const useFetch = (): { fetchInstance: FetchInstance } => {
  const { session } = useSupabase();
  const { backendUrl: configBackendUrl, openAiKey } = defaultBrainConfig;

  const [instance, setInstance] = useState(fetchInstance);

  const baseURL = `${process.env.NEXT_PUBLIC_BACKEND_URL ?? ""}`;
  const backendUrl = configBackendUrl ?? baseURL;

  useEffect(() => {
    setInstance({
      ...fetchInstance,
      get: async (url, headers) =>
        fetchInstance.get(`${backendUrl}${url}`, {
          Authorization: `Bearer ${session?.access_token ?? ""}`,
          "Openai-Api-Key": openAiKey ?? "",
          ...headers,
        }),
      post: async (url, body, headers) =>
        fetchInstance.post(`${backendUrl}${url}`, body, {
          Authorization: `Bearer ${session?.access_token ?? ""}`,
          "Openai-Api-Key": openAiKey ?? "",
          ...headers,
        }),
      put: async (url, body, headers) =>
        fetchInstance.put(`${backendUrl}${url}`, body, {
          Authorization: `Bearer ${session?.access_token ?? ""}`,
          "Openai-Api-Key": openAiKey ?? "",
          ...headers,
        }),
      delete: async (url, headers) =>
        fetchInstance.delete(`${backendUrl}${url}`, {
          Authorization: `Bearer ${session?.access_token ?? ""}`,
          "Openai-Api-Key": openAiKey ?? "",
          ...headers,
        }),
    });
  }, [session, backendUrl, openAiKey]);

  return { fetchInstance: instance };
};
