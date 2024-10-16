import { useMutation, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { useState } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { PUBLIC_BRAINS_KEY } from "@/lib/api/brain/config";
import { IntegrationSettings } from "@/lib/api/brain/types";
import { CreateBrainProps } from "@/lib/components/AddBrainModal/types/types";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useToast } from "@/lib/hooks";

import { useBrainCreationContext } from "../../../brainCreation-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainCreationApi = () => {
  const queryClient = useQueryClient();
  const { publish } = useToast();
  const { t } = useTranslation(["brain", "config"]);
  const { getValues, reset } = useFormContext<CreateBrainProps>();
  const { createBrain: createBrainApi, setCurrentBrainId } = useBrainContext();
  const {
    setIsBrainCreationModalOpened,
    setCreating,
    currentSelectedBrain,
    snippetColor,
    snippetEmoji,
  } = useBrainCreationContext();
  const [fields, setFields] = useState<
    { name: string; type: string; value: string }[]
  >([]);

  const createBrain = async (): Promise<void> => {
    const { name, description } = getValues();
    let integrationSettings: IntegrationSettings | undefined = undefined;

    if (currentSelectedBrain) {
      integrationSettings = {
        integration_id: currentSelectedBrain.id,
        settings: fields.reduce((acc, field) => {
          acc[field.name] = field.value;

          return acc;
        }, {} as { [key: string]: string }),
      };
    }

    const createdBrainId = await createBrainApi({
      brain_type: currentSelectedBrain ? "integration" : "doc",
      name,
      description,
      integration: integrationSettings,
      snippet_color: snippetColor,
      snippet_emoji: snippetEmoji,
    });

    if (createdBrainId === undefined) {
      publish({
        variant: "danger",
        text: t("errorCreatingBrain", { ns: "brain" }),
      });

      return;
    }

    setCurrentBrainId(createdBrainId);
    setIsBrainCreationModalOpened(false);
    setCreating(false);

    reset();

    void queryClient.invalidateQueries({
      queryKey: [PUBLIC_BRAINS_KEY],
    });
  };

  const { mutate, isPending: isBrainCreationPending } = useMutation({
    mutationFn: createBrain,
    onSuccess: () => {
      publish({
        variant: "success",
        text: t("brainCreated", { ns: "brain" }),
      });
    },
    onError: (error: AxiosError) => {
      if (error.response && error.response.status === 429) {
        publish({
          variant: "danger",
          text: "You have reached your maximum amount of brains. Upgrade your plan to create more.",
        });
      } else {
        publish({
          variant: "danger",
          text: t("errorCreatingBrain", { ns: "brain" }),
        });
      }
    },
  });

  return {
    createBrain: mutate,
    isBrainCreationPending,
    fields,
    setFields,
  };
};
