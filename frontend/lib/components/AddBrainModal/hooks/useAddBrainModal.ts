/* eslint-disable max-lines */
import axios from "axios";
import { FormEvent, useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddBrainModal = () => {
  const [isPending, setIsPending] = useState(false);
  const { publish } = useToast();
  const { createBrain } = useBrainContext();
  const { setAsDefaultBrain } = useBrainApi();
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);
  const { config } = useBrainConfig();
  const defaultValues = {
    ...config,
    name: "",
    description: "",
    setDefault: false,
  };

  const { register, getValues, reset, watch, setValue } = useForm({
    defaultValues,
  });

  const openAiKey = watch("openAiKey");
  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  useEffect(() => {
    setValue("maxTokens", Math.min(maxTokens, defineMaxTokens(model)));
  }, [maxTokens, model, setValue]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const { name, description, setDefault } = getValues();

    if (name.trim() === "" || isPending) {
      return;
    }

    try {
      setIsPending(true);
      const createdBrainId = await createBrain({
        name,
        description,
        max_tokens: maxTokens,
        model,
        openai_api_key: openAiKey,
        temperature,
      });

      if (setDefault) {
        if (createdBrainId === undefined) {
          publish({
            variant: "danger",
            text: "Error occurred while creating a brain",
          });

          return;
        }
        await setAsDefaultBrain(createdBrainId);
      }

      setIsShareModalOpen(false);
      reset(defaultValues);
      publish({
        variant: "success",
        text: "Brain created successfully",
      });
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 429) {
        publish({
          variant: "danger",
          text: `${JSON.stringify(
            (
              err.response as {
                data: { detail: string };
              }
            ).data.detail
          )}`,
        });
      } else {
        publish({
          variant: "danger",
          text: `${JSON.stringify(err)}`,
        });
      }
    } finally {
      setIsPending(false);
    }
  };

  return {
    isShareModalOpen,
    setIsShareModalOpen,
    handleSubmit,
    register,
    openAiKey,
    model,
    temperature,
    maxTokens,
    isPending,
  };
};
