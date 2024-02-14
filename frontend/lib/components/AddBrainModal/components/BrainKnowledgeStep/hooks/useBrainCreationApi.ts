import { useMutation, useQueryClient } from "@tanstack/react-query";
import { UUID } from "crypto";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { PUBLIC_BRAINS_KEY } from "@/lib/api/brain/config";
import { CreateBrainProps } from "@/lib/components/AddBrainModal/types/types";
import { useKnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput/hooks/useKnowledgeToFeedInput.ts";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useToast } from "@/lib/hooks";
import { useKnowledgeToFeedFilesAndUrls } from "@/lib/hooks/useKnowledgeToFeed";

import { useBrainCreationContext } from "../../../brainCreation-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainCreationApi = () => {
  const queryClient = useQueryClient();
  const { publish } = useToast();
  const { t } = useTranslation(["brain", "config"]);
  const { files, urls } = useKnowledgeToFeedFilesAndUrls();
  const { getValues, reset } = useFormContext<CreateBrainProps>();
  const { setKnowledgeToFeed } = useKnowledgeToFeedContext();
  const { createBrain: createBrainApi, setCurrentBrainId } = useBrainContext();
  const { crawlWebsiteHandler, uploadFileHandler } = useKnowledgeToFeedInput();
  const { setIsBrainCreationModalOpened, setCreating } =
    useBrainCreationContext();

  const handleFeedBrain = async (brainId: UUID): Promise<void> => {
    const uploadPromises = files.map((file) =>
      uploadFileHandler(file, brainId)
    );
    const crawlPromises = urls.map((url) => crawlWebsiteHandler(url, brainId));

    await Promise.all([...uploadPromises, ...crawlPromises]);
    setKnowledgeToFeed([]);
  };

  const createBrain = async (): Promise<void> => {
    const {
      name,
      description,
      brain_definition,
      brain_secrets_values,
      status,
      brain_type,
      connected_brains_ids,
    } = getValues();

    const createdBrainId = await createBrainApi({
      name,
      description,
      status,
      brain_type,
      brain_definition: brain_type === "api" ? brain_definition : undefined,
      brain_secrets_values:
        brain_type === "api" ? brain_secrets_values : undefined,
      connected_brains_ids:
        brain_type === "composite" ? connected_brains_ids : undefined,
    });

    if (createdBrainId === undefined) {
      publish({
        variant: "danger",
        text: t("errorCreatingBrain", { ns: "brain" }),
      });

      return;
    }
    if (brain_type === "doc") {
      void handleFeedBrain(createdBrainId);
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
    onError: () => {
      publish({
        variant: "danger",
        text: t("errorCreatingBrain", { ns: "brain" }),
      });
    },
  });

  return {
    createBrain: mutate,
    isBrainCreationPending,
  };
};
