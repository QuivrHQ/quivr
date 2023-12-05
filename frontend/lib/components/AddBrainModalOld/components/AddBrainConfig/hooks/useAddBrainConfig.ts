/* eslint-disable max-lines */
import { useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useEffect, useState } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { PUBLIC_BRAINS_KEY } from "@/lib/api/brain/config";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { USER_DATA_KEY } from "@/lib/api/user/config";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { getAccessibleModels } from "@/lib/helpers/getAccessibleModels";
import { useToast } from "@/lib/hooks";

import { CreateBrainProps } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddBrainConfig = () => {
  const { t } = useTranslation(["brain", "config"]);
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

  const { data: userData } = useQuery({
    queryKey: [USER_DATA_KEY],
    queryFn: getUser,
  });

  const {
    register,
    getValues,
    reset,
    watch,
    setValue,
    formState: { dirtyFields },
  } = useFormContext<CreateBrainProps>();

  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("max_tokens");
  const status = watch("status");
  const brainType = watch("brain_type");

  const accessibleModels = getAccessibleModels({
    userData,
  });

  useEffect(() => {
    if (status === "public" && dirtyFields.status === true) {
      setIsPublicAccessConfirmationModalOpened(true);
    }
  }, [dirtyFields.status, status]);

  useEffect(() => {
    if (maxTokens !== undefined && model !== undefined) {
      setValue("max_tokens", Math.min(maxTokens, defineMaxTokens(model)));
    }
  }, [maxTokens, model, setValue]);

  const getCreatingBrainPromptId = async (): Promise<string | undefined> => {
    const { prompt } = getValues();

    if (prompt.title.trim() !== "" && prompt.content.trim() !== "") {
      return (await createPrompt(prompt)).id;
    }

    return undefined;
  };

  // eslint-disable-next-line complexity
  const handleSubmit = async () => {
    const {
      name,
      description,
      setDefault,
      brain_definition,
      brain_secrets_values,
    } = getValues();

    if (name.trim() === "" || isPending) {
      publish({
        variant: "danger",
        text: t("nameRequired", { ns: "config" }),
      });

      return;
    }

    if (description.trim() === "") {
      publish({
        variant: "danger",
        text: t("descriptionRequired", { ns: "config" }),
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
        temperature,
        prompt_id,
        status,
        brain_type: brainType,
        brain_definition,
        brain_secrets_values,
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
      reset();
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
    model,
    temperature,
    maxTokens,
    isPending,
    accessibleModels,
    pickPublicPrompt,
    isPublicAccessConfirmationModalOpened,
    onConfirmPublicAccess,
    onCancelPublicAccess,
    register,
  };
};
