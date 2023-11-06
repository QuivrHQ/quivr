/* eslint-disable max-lines */
import axios from "axios";
import { UUID } from "crypto";
import { useEffect, useState } from "react";
import {
  UseFormGetValues,
  UseFormRegister,
  UseFormReset,
  UseFormResetField,
  UseFormSetValue,
} from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useToast } from "@/lib/hooks";
import { BrainConfig } from "@/lib/types/brainConfig";

type DirtyFields<T> = {
  [K in keyof T]?: T[K] extends object
    ? DirtyFields<T[K]>
    : boolean | undefined;
};

export type UsePromptProps = {
  brainId: UUID;
  getValues: UseFormGetValues<BrainConfig>;
  promptId: string | undefined;
  register: UseFormRegister<BrainConfig>;
  reset: UseFormReset<BrainConfig>;
  setValue: UseFormSetValue<BrainConfig>;
  setIsUpdating: (isUpdating: boolean) => void;
  resetField: UseFormResetField<BrainConfig>;
  updateFormValues: () => void;
  dirtyFields: DirtyFields<BrainConfig>;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePrompt = (props: UsePromptProps) => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const { publish } = useToast();
  const { updateBrain } = useBrainApi();
  const { getPrompt, updatePrompt, createPrompt } = usePromptApi();
  const [isRemovingPrompt, setIsRemovingPrompt] = useState(false);
  const { fetchAllBrains } = useBrainContext();

  const {
    brainId,
    dirtyFields,
    getValues,
    promptId,
    register,
    reset,
    setValue,
    resetField,
    updateFormValues,
    setIsUpdating,
  } = props;

  const [currentPromptId, setCurrentPromptId] = useState<string | undefined>(
    promptId
  );

  useEffect(() => {
    setCurrentPromptId(promptId);
  }, [promptId]);

  const fetchPrompt = async () => {
    if (currentPromptId === "" || currentPromptId === undefined) {
      return;
    }

    const prompt = await getPrompt(currentPromptId);
    if (prompt === undefined) {
      return;
    }
    setValue("prompt", prompt);
  };
  useEffect(() => {
    void fetchPrompt();
  }, [currentPromptId]);

  const removeBrainPrompt = async () => {
    try {
      setIsRemovingPrompt(true);
      await updateBrain(brainId, {
        prompt_id: null,
      });
      setValue("prompt", {
        title: "",
        content: "",
      });
      reset();
      void updateFormValues();
      publish({
        variant: "success",
        text: t("promptRemoved", { ns: "config" }),
      });
      setCurrentPromptId(undefined);
    } catch (err) {
      publish({
        variant: "danger",
        text: t("errorRemovingPrompt", { ns: "config" }),
      });
    } finally {
      setIsRemovingPrompt(false);
    }
  };

  const promptHandler = async () => {
    const { prompt } = getValues();

    if (dirtyFields["prompt"] && promptId !== undefined) {
      await updatePrompt(promptId, {
        title: prompt.title,
        content: prompt.content,
      });
    }
  };

  // eslint-disable-next-line complexity
  const submitPrompt = async () => {
    const {
      prompt,
      maxTokens: max_tokens,
      openAiKey: openai_api_key,
      ...otherConfigs
    } = getValues();

    if (!dirtyFields["prompt"]) {
      return;
    }

    if (prompt.content === "" || prompt.title === "") {
      publish({
        variant: "warning",
        text: t("promptFieldsRequired", { ns: "config" }),
      });

      return;
    }

    try {
      if (promptId === "" || promptId === undefined) {
        otherConfigs["prompt_id"] = (
          await createPrompt({
            title: prompt.title,
            content: prompt.content,
          })
        ).id;
        console.log("OTHER CONFIGS", otherConfigs);
        await updateBrain(brainId, {
          ...otherConfigs,
          max_tokens,
          openai_api_key,
        });
        void updateFormValues();
      } else {
        await Promise.all([
          updateBrain(brainId, {
            ...otherConfigs,
            max_tokens,
            openai_api_key,
          }),
          promptHandler(),
        ]);
      }
      void fetchAllBrains();

      publish({
        variant: "success",
        text: t("brainUpdated", { ns: "config" }),
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
      setIsUpdating(false);
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
    register,
    pickPublicPrompt,
    submitPrompt,
    removeBrainPrompt,
    setValue,
    isRemovingPrompt,
    promptId,
    dirtyFields,
    resetField,
  };
};
