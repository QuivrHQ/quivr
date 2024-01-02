import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";
import { useToast } from "@/lib/hooks";

import { useBrainCreationApi } from "./useBrainCreationApi";

type UseBrainCreationHandler = {
  closeBrainCreationModal: () => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainCreationHandler = ({
  closeBrainCreationModal,
}: UseBrainCreationHandler) => {
  const { getValues } = useFormContext<CreateBrainProps>();
  const { publish } = useToast();
  const { t } = useTranslation(["brain", "config"]);

  const { isBrainCreationPending, createBrain } = useBrainCreationApi({
    closeBrainCreationModal,
  });

  const handleCreateBrain = () => {
    const { name, description } = getValues();

    if (name.trim() === "" || isBrainCreationPending) {
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
    createBrain();
  };

  return {
    handleCreateBrain,
    isBrainCreationPending,
  };
};
