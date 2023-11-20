import { UUID } from "crypto";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useToast } from "@/lib/hooks";

type UseApiBrainSecretsInputsProps = {
  brainId: UUID;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useApiBrainSecretsInputs = ({
  brainId,
}: UseApiBrainSecretsInputsProps) => {
  const { t } = useTranslation(["brain"]);
  const { register, getValues } = useForm<Record<string, string>>();
  const { updateBrainSecrets } = useBrainApi();
  const { publish } = useToast();
  const updateSecrets = async () => {
    try {
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
      publish({ text: t("secrets_updated"), variant: "success" });
    } catch (error) {
      publish({ text: t("secrets_update_error"), variant: "danger" });
    }
  };

  return {
    register,
    updateSecrets,
  };
};
