/* eslint-disable complexity */
/* eslint-disable max-lines */
import axios from "axios";
import { UUID } from "crypto";
import { FormEvent, useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider";
import { useBrainProvider } from "@/lib/context/BrainProvider/hooks/useBrainProvider";
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

  const { setAsDefaultBrain, getBrain, updateBrain } = useBrainApi();
  const { config } = useBrainConfig();

  const defaultValues = {
    ...config,
    name: "",
    description: "",
    setDefault: false,
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

  useEffect(() => {
    const fetchBrain = async () => {
      const brain = await getBrain(brainId);
      if (brain === undefined) {
        return;
      }
      reset({
        ...brain,
        maxTokens: brain.max_tokens,
      });
    };
    void fetchBrain();
  }, []);

  const openAiKey = watch("openAiKey");
  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  useEffect(() => {
    setValue("maxTokens", Math.min(maxTokens, defineMaxTokens(model)));
  }, [maxTokens, model, setValue]);

  const setAsDefaultBrainHandler = async () => {
    try {
      setIsSettingHasDefault(true);
      await setAsDefaultBrain(brainId);
      publish({
        variant: "success",
        text: "Brain set as default successfully",
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
    } finally {
      setIsSettingHasDefault(false);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
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

      await updateBrain(brainId, getValues());

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
      setIsUpdating(false);
    }
  };
  const { defaultBrainId } = useBrainProvider();
  const isDefaultBrain = defaultBrainId === brainId;

  return {
    handleSubmit,
    register,
    openAiKey,
    model,
    temperature,
    maxTokens,
    isUpdating,
    hasChanges: Object.keys(dirtyFields).length > 0,
    setAsDefaultBrainHandler,
    isSettingAsDefault,
    isDefaultBrain,
  };
};
