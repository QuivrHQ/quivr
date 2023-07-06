import { useState } from "react";

import { useAxios } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useApiKeyConfig = () => {
  const [apiKey, setApiKey] = useState("");
  const { axiosInstance } = useAxios();
  const { track } = useEventTracking();

  const handleCreateClick = async () => {
    try {
      void track("CREATE_API_KEY");
      const response = await axiosInstance.post<{ api_key: string }>(
        "/api-key"
      ); // replace with your api-key endpoint URL
      setApiKey(response.data.api_key);
    } catch (error) {
      console.error("Error creating API key: ", error);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      void track("COPY_API_KEY");
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  const handleCopyClick = () => {
    if (apiKey !== "") {
      void copyToClipboard(apiKey);
    }
  };

  return {
    handleCreateClick,
    apiKey,
    handleCopyClick,
  };
};
