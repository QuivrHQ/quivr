/* eslint-disable max-lines */
import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import {
  getChatConfigFromLocalStorage,
  saveChatConfigInLocalStorage,
} from "@/lib/api/chat/chat.local";
import { USER_DATA_KEY, USER_IDENTITY_DATA_KEY } from "@/lib/api/user/config";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { defaultBrainConfig } from "@/lib/config/defaultBrainConfig";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { ChatConfig } from "@/lib/context/ChatProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { getAccessibleModels } from "@/lib/helpers/getAccessibleModels";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useConfigModal = (chatId?: string) => {
  const { publish } = useToast();
  const [isConfigModalOpen, setIsConfigModalOpen] = useState(false);
  const { getBrain } = useBrainApi();
  const { currentBrain } = useBrainContext();
  const { getUser, getUserIdentity } = useUserApi();

  const { data: userData } = useQuery({
    queryKey: [USER_DATA_KEY],
    queryFn: getUser,
  });
  const { data: userIdentityData } = useQuery({
    queryKey: [USER_IDENTITY_DATA_KEY],
    queryFn: getUserIdentity,
  });

  const defaultValues: ChatConfig = {};

  const { register, watch, setValue } = useForm({
    defaultValues,
  });

  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  const accessibleModels = getAccessibleModels({
    openAiKey: userIdentityData?.openai_api_key,
    userData,
  });

  useEffect(() => {
    const fetchChatConfig = async () => {
      if (chatId === undefined) {
        return;
      }

      const chatConfig = getChatConfigFromLocalStorage(chatId);
      if (chatConfig !== undefined) {
        setValue("model", chatConfig.model);
        setValue("temperature", chatConfig.temperature);
        setValue("maxTokens", chatConfig.maxTokens);
      } else {
        if (currentBrain === undefined) {
          return;
        }

        const relatedBrainConfig = await getBrain(currentBrain.id);
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
    };
    void fetchChatConfig();
  }, []);

  useEffect(() => {
    if (maxTokens === undefined || model === undefined) {
      return;
    }

    setValue("maxTokens", Math.min(maxTokens, defineMaxTokens(model)));
  }, [maxTokens, model, setValue]);

  const handleSubmit = () => {
    if (chatId === undefined) {
      return;
    }
    try {
      saveChatConfigInLocalStorage(chatId, {
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
  };

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
