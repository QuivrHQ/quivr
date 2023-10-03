/* eslint-disable max-lines */
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { validateOpenAIKey } from "@/app/brains-management/[brainId]/components/BrainManagementTabs/components/SettingsTab/utils/validateOpenAIKey";
import { useAuthApi } from "@/lib/api/auth/useAuthApi";
import { USER_IDENTITY_DATA_KEY } from "@/lib/api/user/config";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { UserIdentity } from "@/lib/api/user/user";
import copyToClipboard from "@/lib/helpers/copyToClipboard";
import { useToast } from "@/lib/hooks";
import { useGAnalyticsEventTracker } from "@/services/analytics/google/useGAnalyticsEventTracker";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

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
  const { t } = useTranslation(["config"]);
  const queryClient = useQueryClient();
  const { data: userData } = useQuery({
    queryKey: [USER_IDENTITY_DATA_KEY],
    queryFn: getUserIdentity,
  });
  const { eventTracker: gaEventTracker } = useGAnalyticsEventTracker({
    category: "QUIVR_API_KEY",
  });

  useEffect(() => {
    if (userData !== undefined) {
      setUserIdentity(userData);
    }
  }, [userData]);

  const handleCreateClick = async () => {
    try {
      void track("CREATE_API_KEY");
      gaEventTracker?.({ action: "CREATE_API_KEY" });
      const createdApiKey = await createApiKey();
      setApiKey(createdApiKey);
    } catch (error) {
      console.error("Error creating API key: ", error);
    }
  };

  const handleCopyClick = () => {
    if (apiKey !== "") {
      void track("COPY_API_KEY");
      gaEventTracker?.({ action: "COPY_API_KEY" });

      void copyToClipboard(apiKey);
    }
  };

  const changeOpenAiApiKey = async () => {
    try {
      setChangeOpenAiApiKeyRequestPending(true);

      if (
        openAiApiKey !== undefined &&
        openAiApiKey !== null &&
        !(await validateOpenAIKey(
          openAiApiKey,
          {
            badApiKeyError: t("incorrectApiKey", { ns: "config" }),
            invalidApiKeyError: t("invalidApiKeyError", { ns: "config" }),
          },
          publish
        ))
      ) {
        setChangeOpenAiApiKeyRequestPending(false);

        return;
      }

      await updateUserIdentity({
        openai_api_key: openAiApiKey,
      });
      void queryClient.invalidateQueries({
        queryKey: [USER_IDENTITY_DATA_KEY],
      });

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

      void queryClient.invalidateQueries({
        queryKey: [USER_IDENTITY_DATA_KEY],
      });
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
