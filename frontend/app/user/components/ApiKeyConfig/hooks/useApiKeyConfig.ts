/* eslint-disable max-lines */
import { useEffect, useState } from "react";

import { useAuthApi } from "@/lib/api/auth/useAuthApi";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { UserIdentity } from "@/lib/api/user/user";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useApiKeyConfig = () => {
  const [apiKey, setApiKey] = useState("");
  const [openAiApiKey, setOpenAiApiKey] = useState<string | null>();
  const [
    changeOpenAiApiKeyRequestPending,
    setChangeOpenAiApiKeyRequestPending,
  ] = useState(false);
  const { updateUserIdentity, getUserIdentity } = useUserApi();
  const { track } = useEventTracking();
  const { createApiKey } = useAuthApi();
  const { publish } = useToast();
  const [userIdentity, setUserIdentity] = useState<UserIdentity>();

  const fetchUserIdentity = async () => {
    setUserIdentity(await getUserIdentity());
  };
  useEffect(() => {
    void fetchUserIdentity();
  }, []);

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

  const changeOpenAiApiKey = async () => {
    try {
      setChangeOpenAiApiKeyRequestPending(true);
      await updateUserIdentity({
        openai_api_key: openAiApiKey,
      });
      void fetchUserIdentity();
      publish({
        variant: "success",
        text: "OpenAI API Key updated",
      });
    } catch (error) {
      console.error(error);
    } finally {
      setChangeOpenAiApiKeyRequestPending(false);
    }
  };

  const removeOpenAiApiKey = async () => {
    try {
      setChangeOpenAiApiKeyRequestPending(true);
      await updateUserIdentity({
        openai_api_key: null,
      });

      publish({
        variant: "success",
        text: "OpenAI API Key removed",
      });

      void fetchUserIdentity();
    } catch (error) {
      console.error(error);
    } finally {
      setChangeOpenAiApiKeyRequestPending(false);
    }
  };

  useEffect(() => {
    if (userIdentity?.openai_api_key !== undefined) {
      setOpenAiApiKey(userIdentity.openai_api_key);
    }
  }, [userIdentity]);

  const hasOpenAiApiKey =
    userIdentity?.openai_api_key !== null &&
    userIdentity?.openai_api_key !== undefined &&
    userIdentity.openai_api_key !== "";

  return {
    handleCreateClick,
    apiKey,
    handleCopyClick,
    openAiApiKey,
    setOpenAiApiKey,
    changeOpenAiApiKey,
    changeOpenAiApiKeyRequestPending,
    userIdentity,
    removeOpenAiApiKey,
    hasOpenAiApiKey,
  };
};
