/* eslint-disable max-lines */
import { FormEvent, useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import {
  getChatConfigFromLocalStorage,
  saveChatConfigInLocalStorage,
} from "@/lib/api/chat/chat.local";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { ChatConfig } from "@/lib/context/ChatProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useConfigModal = (chatId?: string) => {
  const { publish } = useToast();
  const [isConfigModalOpen, setIsConfigModalOpen] = useState(false);
  const { config } = useBrainConfig();
  const { getBrain } = useBrainApi();
  const { currentBrain } = useBrainContext();

  const defaultValues: ChatConfig = {};

  const { register, watch, setValue } = useForm({
    defaultValues,
  });

  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

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
        setValue("model", relatedBrainConfig.model ?? config.model);
        setValue(
          "temperature",
          relatedBrainConfig.temperature ?? config.temperature
        );
        setValue(
          "maxTokens",
          relatedBrainConfig.max_tokens ?? config.maxTokens
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

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
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
        text: "An error occured while updating chat config",
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
  };
};
