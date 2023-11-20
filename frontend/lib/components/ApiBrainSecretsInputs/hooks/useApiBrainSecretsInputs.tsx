import { useMutation } from "@tanstack/react-query";
import { UUID } from "crypto";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useToast } from "@/lib/hooks";

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
  const { register, getValues } = useForm<Record<string, string>>();
  const { updateBrainSecrets } = useBrainApi();
  const { publish } = useToast();

  const updateSecretsHandler = async () => {
    const values = getValues();
    const nonEmptyValues = Object.entries(values).reduce(
      (acc, [key, value]) => {
        if (value !== "") {
          acc[key] = value;
        }

        return acc;
      },
      {} as Record<string, string>
    );
    await updateBrainSecrets(brainId, nonEmptyValues);
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
  };
};
