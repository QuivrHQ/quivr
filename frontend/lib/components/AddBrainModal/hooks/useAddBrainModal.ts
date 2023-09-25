/* eslint-disable */
import axios from "axios";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { PUBLIC_BRAINS_KEY } from "@/lib/api/brain/config";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { USER_DATA_KEY } from "@/lib/api/user/config";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { defaultBrainConfig } from "@/lib/config/defaultBrainConfig";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { getAccessibleModels } from "@/lib/helpers/getAccessibleModels";
import { useToast } from "@/lib/hooks";
import { BrainStatus } from "@/lib/types/brainConfig";
import { useQuery, useQueryClient } from "@tanstack/react-query";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddBrainModal = () => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const [isPending, setIsPending] = useState(false);
  const { publish } = useToast();
  const { createBrain, setCurrentBrainId } = useBrainContext();
  const { setAsDefaultBrain } = useBrainApi();
  const { createPrompt } = usePromptApi();
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);
  const [
    isPublicAccessConfirmationModalOpened,
    setIsPublicAccessConfirmationModalOpened,
  ] = useState(false);
  const { getUser } = useUserApi();
  const queryClient = useQueryClient();

  const brainStatusOptions: {
    label: string;
    value: BrainStatus;
  }[] = [
    {
      label: t("private_brain_label", { ns: "brain" }),
      value: "private",
    },
    {
      label: t("public_brain_label", { ns: "brain" }),
      value: "public",
    },
  ];

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

  const {
    register,
    getValues,
    reset,
    watch,
    setValue,
    formState: { dirtyFields },
  } = useForm({
    defaultValues,
  });

  const openAiKey = watch("openAiKey");
  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");
  const status = watch("status");

  const accessibleModels = getAccessibleModels({
    openAiKey,
    userData,
  });

  useEffect(() => {
    if (status === "public" && dirtyFields.status) {
      setIsPublicAccessConfirmationModalOpened(true);
    }
  }, [status]);

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
        status,
      });

      if (createdBrainId === undefined) {
        publish({
          variant: "danger",
          text: t("errorCreatingBrain", { ns: "brain" }),
        });

        return;
      }

      setCurrentBrainId(createdBrainId);

      if (setDefault) {
        await setAsDefaultBrain(createdBrainId);
      }

      setIsShareModalOpen(false);
      reset(defaultValues);
      publish({
        variant: "success",
        text: t("brainCreated", { ns: "brain" }),
      });
      void queryClient.invalidateQueries({
        queryKey: [PUBLIC_BRAINS_KEY],
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

  const onConfirmPublicAccess = () => {
    setIsPublicAccessConfirmationModalOpened(false);
  };

  const onCancelPublicAccess = () => {
    setValue("status", "private", {
      shouldDirty: true,
    });
    setIsPublicAccessConfirmationModalOpened(false);
  };

  return {
    isShareModalOpen,
    setIsShareModalOpen,
    handleSubmit,
    register,
    model,
    temperature,
    maxTokens,
    isPending,
    accessibleModels,
    pickPublicPrompt,
    brainStatusOptions,
    status,
    isPublicAccessConfirmationModalOpened,
    onConfirmPublicAccess,
    onCancelPublicAccess,
  };
};
