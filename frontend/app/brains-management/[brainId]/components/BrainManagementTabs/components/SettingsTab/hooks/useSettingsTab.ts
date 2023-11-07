/* eslint-disable complexity */
/* eslint-disable max-lines */
import axios from "axios";
import { UUID } from "crypto";
import { useCallback, useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { Brain } from "@/lib/context/BrainProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { getAccessibleModels } from "@/lib/helpers/getAccessibleModels";
import { useToast } from "@/lib/hooks";
import { useUserData } from "@/lib/hooks/useUserData";
import { BrainStatus } from "@/lib/types/brainConfig";

import { useBrainFormState } from "./useBrainFormState";
import { checkBrainName } from "../utils/checkBrainName";
import { checkOpenAiKey } from "../utils/checkOpenAiKey";

type UseSettingsTabProps = {
  brainId: UUID;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSettingsTab = ({ brainId }: UseSettingsTabProps) => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isSettingAsDefault, setIsSettingAsDefault] = useState(false);
  const { publish } = useToast();
  const formRef = useRef<HTMLFormElement>(null);
  const { setAsDefaultBrain, updateBrain } = useBrainApi();
  const { fetchAllBrains, fetchDefaultBrain } = useBrainContext();
  const { userData } = useUserData();

  const {
    brain,
    dirtyFields,
    getValues,
    maxTokens,
    promptId,
    register,
    reset,
    setValue,
    openAiKey,
    model,
    temperature,
    status,
    isDefaultBrain,
    resetField,
  } = useBrainFormState({
    brainId,
  });

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

  const accessibleModels = getAccessibleModels({
    openAiKey,
    userData,
  });

  const updateFormValues = useCallback(() => {
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

      if (brainKey === "openai_api_key") {
        setValue("openAiKey", brain["openai_api_key"] ?? "");
        continue;
      }

      // @ts-expect-error bad type inference from typescript
      // eslint-disable-next-line
      if (Boolean(brain[key])) setValue(key, brain[key]);
    }

    setTimeout(() => {
      if (brain.model !== undefined && brain.model !== null) {
        setValue("model", brain.model);
      }
    }, 50);
  }, [brain, setValue]);

  useEffect(() => {
    updateFormValues();
  }, [brain, updateFormValues]);

  useEffect(() => {
    setValue("maxTokens", Math.min(maxTokens, defineMaxTokens(model)));
  }, [maxTokens, model, setValue]);

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === "Enter") {
        event.preventDefault();
        void handleSubmit(true);
      }
    };

    formRef.current?.addEventListener("keydown", handleKeyPress);

    return () => {
      formRef.current?.removeEventListener("keydown", handleKeyPress);
    };
  }, [formRef.current]);

  const setAsDefaultBrainHandler = async () => {
    try {
      setIsSettingAsDefault(true);
      await setAsDefaultBrain(brainId);
      publish({
        variant: "success",
        text: t("defaultBrainSet", { ns: "config" }),
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
      setIsSettingAsDefault(false);
    }
  };

  const handleSubmit = async (checkDirty: boolean) => {
    const hasChanges = Object.keys(dirtyFields).length > 0;
    if (!hasChanges && checkDirty) {
      return;
    }
    const { name, openAiKey: openai_api_key } = getValues();

    checkBrainName(name, publish, t);
    await checkOpenAiKey(openai_api_key, publish, t);

    try {
      setIsUpdating(true);
      const { maxTokens: max_tokens, ...otherConfigs } = getValues();

      await updateBrain(brainId, {
        ...otherConfigs,
        max_tokens,
        openai_api_key,
        prompt_id:
          otherConfigs["prompt_id"] !== ""
            ? otherConfigs["prompt_id"]
            : undefined,
      });

      publish({
        variant: "success",
        text: t("brainUpdated", { ns: "config" }),
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

  return {
    handleSubmit,
    register,
    setAsDefaultBrainHandler,
    setValue,
    brain,
    model,
    temperature,
    maxTokens,
    isUpdating,
    isSettingAsDefault,
    isDefaultBrain,
    formRef,
    promptId,
    accessibleModels,
    brainStatusOptions,
    status,
    dirtyFields,
    resetField,
    updateFormValues,
    reset,
    getValues,
    setIsUpdating,
  };
};
