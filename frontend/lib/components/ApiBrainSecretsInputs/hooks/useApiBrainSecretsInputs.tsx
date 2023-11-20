import { useMutation } from "@tanstack/react-query";
import { UUID } from "crypto";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useToast } from "@/lib/hooks";

import { getNonEmptyValuesFromDict } from "../utils/getNonEmptyValuesFromDict";

type UseApiBrainSecretsInputsProps = {
  brainId: UUID;
  onUpdate?: () => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useApiBrainSecretsInputs = ({
  brainId,
  onUpdate,
}: UseApiBrainSecretsInputsProps) => {
  const { t } = useTranslation(["brain"]);
  const { register, watch } = useForm<Record<string, string>>();
  const { updateBrainSecrets } = useBrainApi();
  const { publish } = useToast();

  const values = watch();

  const [isUpdateButtonDisabled, setIsUpdateButtonDisabled] = useState(false);

  useEffect(() => {
    const nonEmptyValues = getNonEmptyValuesFromDict(values);
    setIsUpdateButtonDisabled(Object.keys(nonEmptyValues).length === 0);
  }, [values]);

  const updateSecretsHandler = async () => {
    await updateBrainSecrets(brainId, getNonEmptyValuesFromDict(values));
    onUpdate?.();
  };

  const { mutate: updateSecrets, isPending } = useMutation({
    mutationFn: updateSecretsHandler,
    onSuccess: () => {
      publish({ text: t("secrets_updated"), variant: "success" });
    },
    onError: () => {
      publish({ text: t("secrets_update_error"), variant: "danger" });
    },
  });

  return {
    register,
    updateSecrets,
    isPending,
    isUpdateButtonDisabled,
  };
};
