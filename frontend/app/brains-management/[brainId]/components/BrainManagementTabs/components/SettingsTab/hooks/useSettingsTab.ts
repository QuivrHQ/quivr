/* eslint-disable complexity */
/* eslint-disable max-lines */
import axios from "axios";
import { UUID } from "crypto";
import { useEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { Brain } from "@/lib/context/BrainProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";
import { useToast } from "@/lib/hooks";

type UseSettingsTabProps = {
  brainId: UUID;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSettingsTab = ({ brainId }: UseSettingsTabProps) => {
  const [isUpdating, setIsUpdating] = useState(false);
  const [isSettingAsDefault, setIsSettingHasDefault] = useState(false);
  const { publish } = useToast();
  const formRef = useRef<HTMLFormElement>(null);
  const { setAsDefaultBrain, getBrain, updateBrain } = useBrainApi();
  const { config } = useBrainConfig();
  const { fetchAllBrains, fetchDefaultBrain, defaultBrainId } =
    useBrainContext();
  const { getPrompt, updatePrompt, createPrompt } = usePromptApi();

  const defaultValues = {
    ...config,
    name: "",
    description: "",
    setDefault: false,
    prompt_id: "",
    prompt: {
      title: "",
      content: "",
    },
  };

  const {
    register,
    getValues,
    watch,
    setValue,
    reset,
    formState: { dirtyFields },
  } = useForm({
    defaultValues,
  });

  const isDefaultBrain = defaultBrainId === brainId;
  const promptId = watch("prompt_id");
  const openAiKey = watch("openAiKey");
  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  const fetchBrain = async () => {
    const brain = await getBrain(brainId);
    if (brain === undefined) {
      return;
    }

    for (const key in brain) {
      const brainKey = key as keyof Brain;
      if (!(key in brain)) {
        return;
      }

      if (brainKey === "max_tokens" && brain["max_tokens"] !== undefined) {
        setValue("maxTokens", brain["max_tokens"]);
        continue;
      }

      if (
        brainKey === "openai_api_key" &&
        brain["openai_api_key"] !== undefined
      ) {
        setValue("openAiKey", brain["openai_api_key"]);
        continue;
      }

      // @ts-expect-error bad type inference from typescript
      // eslint-disable-next-line
      if (Boolean(brain[key])) setValue(key, brain[key]);
    }
  };
  useEffect(() => {
    void fetchBrain();
  }, []);

  useEffect(() => {
    setValue("maxTokens", Math.min(maxTokens, defineMaxTokens(model)));
  }, [maxTokens, model, setValue]);

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === "Enter") {
        event.preventDefault();
        void handleSubmit();
      }
    };

    formRef.current?.addEventListener("keydown", handleKeyPress);

    return () => {
      formRef.current?.removeEventListener("keydown", handleKeyPress);
    };
  }, [formRef.current]);

  const fetchPrompt = async () => {
    if (promptId === "") {
      return;
    }

    const prompt = await getPrompt(promptId);
    if (prompt === undefined) {
      return;
    }
    setValue("prompt", prompt);
  };
  useEffect(() => {
    void fetchPrompt();
  }, [promptId]);

  const setAsDefaultBrainHandler = async () => {
    try {
      setIsSettingHasDefault(true);
      await setAsDefaultBrain(brainId);
      publish({
        variant: "success",
        text: "Brain set as default successfully",
      });
      void fetchAllBrains();
      void fetchDefaultBrain();
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
    } finally {
      setIsSettingHasDefault(false);
    }
  };

  const removeBrainPrompt = async () => {
    try {
      setIsUpdating(true);
      await updateBrain(brainId, {
        prompt_id: null,
      });
      setValue("prompt", {
        title: "",
        content: "",
      });
      reset();
      void fetchBrain();
      publish({
        variant: "success",
        text: "Prompt removed successfully",
      });
    } catch (err) {
      publish({
        variant: "danger",
        text: "Error while removing prompt",
      });
    } finally {
      setIsUpdating(false);
    }
  };

  const promptHandler = async () => {
    const { prompt } = getValues();

    if (dirtyFields["prompt"]) {
      await updatePrompt(promptId, {
        title: prompt.title,
        content: prompt.content,
      });
    }
  };

  const handleSubmit = async () => {
    const hasChanges = Object.keys(dirtyFields).length > 0;

    if (!hasChanges) {
      return;
    }
    const { name: isNameDirty } = dirtyFields;
    const { name } = getValues();
    if (isNameDirty !== undefined && isNameDirty && name.trim() === "") {
      publish({
        variant: "danger",
        text: "Name is required",
      });

      return;
    }

    try {
      setIsUpdating(true);

      const {
        maxTokens: max_tokens,
        openAiKey: openai_api_key,
        prompt,
        ...otherConfigs
      } = getValues();

      if (
        dirtyFields["prompt"] &&
        (prompt.content === "" || prompt.title === "")
      ) {
        publish({
          variant: "warning",
          text: "Prompt title and content are required",
        });

        return;
      }

      if (dirtyFields["prompt"]) {
        if (promptId === "") {
          otherConfigs["prompt_id"] = (
            await createPrompt({
              title: prompt.title,
              content: prompt.content,
            })
          ).id;
          await updateBrain(brainId, {
            ...otherConfigs,
            max_tokens,
            openai_api_key,
          });
          void fetchBrain();
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
      } else {
        await updateBrain(brainId, {
          ...otherConfigs,
          max_tokens,
          openai_api_key,
          prompt_id:
            otherConfigs["prompt_id"] !== ""
              ? otherConfigs["prompt_id"]
              : undefined,
        });
      }

      publish({
        variant: "success",
        text: "Brain updated successfully",
      });
      void fetchAllBrains();
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
    handleSubmit,
    register,
    openAiKey,
    model,
    temperature,
    maxTokens,
    isUpdating,
    setAsDefaultBrainHandler,
    isSettingAsDefault,
    isDefaultBrain,
    formRef,
    promptId,
    removeBrainPrompt,
    pickPublicPrompt,
  };
};
