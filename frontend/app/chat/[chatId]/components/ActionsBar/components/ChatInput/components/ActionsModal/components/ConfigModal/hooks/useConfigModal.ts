/* eslint-disable max-lines */
import { useCallback, useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { useLocalStorageChatConfig } from "@/app/chat/[chatId]/hooks/useLocalStorageChatConfig";
import { saveChatsConfigInLocalStorage } from "@/lib/api/chat/chat.local";
import { ChatConfig } from "@/lib/context/ChatProvider/types";
import { getAccessibleModels } from "@/lib/helpers/getAccessibleModels";
import { useToast } from "@/lib/hooks";
import { useUserData } from "@/lib/hooks/useUserData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useConfigModal = () => {
  const { publish } = useToast();
  const [isConfigModalOpen, setIsConfigModalOpen] = useState(false);
  const { chatConfig } = useLocalStorageChatConfig();
  const { userData } = useUserData();

  const { register, watch, setValue } = useForm<ChatConfig>({
    defaultValues: {
      model: chatConfig.model,
      temperature: chatConfig.temperature ?? 0,
      maxTokens: chatConfig.maxTokens ?? 3000,
    },
  });

  const model = watch("model");

  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  const accessibleModels = getAccessibleModels({
    userData,
  });

  useEffect(() => {
    if (chatConfig.model !== undefined) {
      setValue("model", chatConfig.model);
    }
    if (chatConfig.temperature !== undefined) {
      setValue("temperature", chatConfig.temperature);
    }
    if (chatConfig.maxTokens !== undefined) {
      setValue("maxTokens", chatConfig.maxTokens);
    }
  }, [chatConfig.maxTokens, chatConfig.model, chatConfig.temperature]);

  const handleSubmit = useCallback(() => {
    try {
      saveChatsConfigInLocalStorage({
        maxTokens,
        model: model.length > 0 ? model : undefined,
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
