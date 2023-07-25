import { useState } from "react";

import { useAuthApi } from "@/lib/api/auth/useAuthApi";
import { useEventTracking } from "@/services/analytics/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useApiKeyConfig = () => {
  const [apiKey, setApiKey] = useState("");
  const { track } = useEventTracking();
  const { createApiKey } = useAuthApi();

  const handleCreateClick = async () => {
    try {
      void track("CREATE_API_KEY");
      const createdApiKey = await createApiKey();
      setApiKey(createdApiKey);
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
