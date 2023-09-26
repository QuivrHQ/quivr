/* eslint-disable max-lines */
import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import {
  getChatsConfigFromLocalStorage,
  saveChatsConfigInLocalStorage,
} from "@/lib/api/chat/chat.local";
import { USER_DATA_KEY, USER_IDENTITY_DATA_KEY } from "@/lib/api/user/config";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { defaultBrainConfig } from "@/lib/config/defaultBrainConfig";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { ChatConfig } from "@/lib/context/ChatProvider/types";
import { getAccessibleModels } from "@/lib/helpers/getAccessibleModels";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useConfigModal = () => {
  const { publish } = useToast();
  const [isConfigModalOpen, setIsConfigModalOpen] = useState(false);
  const { getBrain } = useBrainApi();
  const { currentBrainId } = useBrainContext();
  const { getUser, getUserIdentity } = useUserApi();

  const { data: userData } = useQuery({
    queryKey: [USER_DATA_KEY],
    queryFn: getUser,
  });
  const { data: userIdentityData } = useQuery({
    queryKey: [USER_IDENTITY_DATA_KEY],
    queryFn: getUserIdentity,
  });

  const { register, watch, setValue } = useForm<ChatConfig>({
    defaultValues: {
      model: defaultBrainConfig.model,
      temperature: defaultBrainConfig.temperature,
      maxTokens: defaultBrainConfig.maxTokens,
    },
  });

  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  const accessibleModels = getAccessibleModels({
    openAiKey: userIdentityData?.openai_api_key,
    userData,
  });

  const fetchChatConfig = useCallback(async () => {
    const chatConfig = getChatsConfigFromLocalStorage();
    if (chatConfig !== undefined) {
      setValue("model", chatConfig.model);
      setValue("temperature", chatConfig.temperature);
      setValue("maxTokens", chatConfig.maxTokens);
    } else {
      if (currentBrainId === null) {
        return;
      }
      const relatedBrainConfig = await getBrain(currentBrainId);

      if (relatedBrainConfig === undefined) {
        return;
      }
      setValue("model", relatedBrainConfig.model ?? defaultBrainConfig.model);
      setValue(
        "temperature",
        relatedBrainConfig.temperature ?? defaultBrainConfig.temperature
      );
      setValue(
        "maxTokens",
        relatedBrainConfig.max_tokens ?? defaultBrainConfig.maxTokens
      );
    }
  }, []);

  useEffect(() => {
    void fetchChatConfig();
  }, [fetchChatConfig]);

  const handleSubmit = useCallback(() => {
    try {
      saveChatsConfigInLocalStorage({
        maxTokens,
        model,
        temperature,
      });

      publish({
        variant: "success",
        text: "Chat config successfully updated",
      });
    } catch (err) {
      publish({
        variant: "danger",
        text: "An error occurred while updating chat config",
      });
    }
  }, [maxTokens, model, publish, temperature]);

  return {
    isConfigModalOpen,
    setIsConfigModalOpen,
    handleSubmit,
    register,
    model,
    temperature,
    maxTokens,
    accessibleModels,
  };
};
