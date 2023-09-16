/* eslint-disable */
import axios from "axios";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { USER_DATA_KEY } from "@/lib/api/user/config";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { defaultBrainConfig } from "@/lib/config/defaultBrainConfig";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { getAccessibleModels } from "@/lib/helpers/getAccessibleModels";
import { useToast } from "@/lib/hooks";
import { useQuery } from "@tanstack/react-query";




// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddBrainModal = () => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const [isPending, setIsPending] = useState(false);
  const { publish } = useToast();
  const { createBrain, setActiveBrain } = useBrainContext();
  const { setAsDefaultBrain } = useBrainApi();
  const { createPrompt } = usePromptApi();
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);

  const { getUser } = useUserApi();


  const { data: userData } = useQuery({
    queryKey: [USER_DATA_KEY],
    queryFn: getUser,
  });
  const defaultValues = {
    ...defaultBrainConfig,
    name: "",
    description: "",
    setDefault: false,
    prompt: {
      title: "",
      content: "",
    },
  };

  

  

  const { register, getValues, reset, watch, setValue } = useForm({
    defaultValues,
  });

  const openAiKey = watch("openAiKey");
  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  const accessibleModels = getAccessibleModels({
    openAiKey,
    userData,
  });

  useEffect(() => {
    setValue("maxTokens", Math.min(maxTokens, defineMaxTokens(model)));
  }, [maxTokens, model, setValue]);

  const getCreatingBrainPromptId = async (): Promise<string | undefined> => {
    const { prompt } = getValues();

    if (prompt.title.trim() !== "" && prompt.content.trim() !== "") {
      return (await createPrompt(prompt)).id;
    }

    return undefined;
  };

  const handleSubmit = async () => {
    const { name, description, setDefault } = getValues();

    if (name.trim() === "" || isPending) {
      publish({
        variant: "danger",
        text: t("nameRequired", { ns: "config" }),
      });

      return;
    }

    try {
      setIsPending(true);

      const prompt_id = await getCreatingBrainPromptId();

      const createdBrainId = await createBrain({
        name,
        description,
        max_tokens: maxTokens,
        model,
        openai_api_key: openAiKey,
        temperature,
        prompt_id,
      });

      if (createdBrainId === undefined) {
        publish({
          variant: "danger",
          text: t("errorCreatingBrain", { ns: "brain" }),
        });

        return;
      }

      setActiveBrain({
        id: createdBrainId,
        name,
      });

      if (setDefault) {
        await setAsDefaultBrain(createdBrainId);
      }

      setIsShareModalOpen(false);
      reset(defaultValues);
      publish({
        variant: "success",
        text: t("brainCreated", { ns: "brain" }),
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

        return;
      }
      publish({
        variant: "danger",
        text: `${JSON.stringify(err)}`,
      });
    } finally {
      setIsPending(false);
    }
  };

  const pickPublicPrompt = ({
    title,
    content,
  }: {
    title: string;
    content: string;
  }): void => {
    setValue("prompt.title", title, {
      shouldDirty: true,
    });
    setValue("prompt.content", content, {
      shouldDirty: true,
    });
  };

  return {
    isShareModalOpen,
    setIsShareModalOpen,
    handleSubmit,
    register,
    openAiKey: openAiKey === "" ? undefined : openAiKey,
    model,
    temperature,
    maxTokens,
    isPending,
    accessibleModels,
    pickPublicPrompt,
  };
};
