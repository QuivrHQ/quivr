import { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { TextArea } from "@/lib/components/ui/TextArea";

import { PublicAccessConfirmationModal } from "./components/PublicAccessConfirmationModal";
import { useBrainParamsStep } from "./hooks/useBrainParamsStep";
import { usePublicAccessConfirmationModal } from "./hooks/usePublicAccessConfirmationModal";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";
import { useBrainTypeSelectionStep } from "../BrainTypeSelectionStep/hooks/useBrainTypeSelectionStep";

type BrainParamsStepProps = {
  onCancelBrainCreation: () => void;
};

export const BrainParamsStep = ({
  onCancelBrainCreation,
}: BrainParamsStepProps): JSX.Element => {
  const { goToNextStep, goToPreviousStep, currentStep } =
    useBrainCreationSteps();
  const { register } = useBrainTypeSelectionStep();
  const { t } = useTranslation(["translation", "brain", "config"]);
  const { isNextButtonDisabled } = useBrainParamsStep();
  const {
    isPublicAccessConfirmationModalOpened,
    onCancelPublicAccess,
    onConfirmPublicAccess,
  } = usePublicAccessConfirmationModal();

  if (currentStep !== "BRAIN_PARAMS") {
    return <Fragment />;
  }

  return (
    <>
      <Field
        label={t("brainName", { ns: "brain" })}
        autoFocus
        placeholder={t("brainNamePlaceholder", { ns: "brain" })}
        autoComplete="off"
        className="flex-1"
        required
        {...register("name")}
      />
      <TextArea
        label={t("brainDescription", { ns: "brain" })}
        placeholder={t("brainDescriptionPlaceholder", { ns: "brain" })}
        autoComplete="off"
        className="flex-1 m-3"
        required
        {...register("description")}
      />
      <div className="flex flex-row justify-between items-center flex-1 mt-10 w-full">
        <Button
          type="button"
          variant="tertiary"
          onClick={onCancelBrainCreation}
          className="text-primary"
        >
          {t("cancel", { ns: "translation" })}
        </Button>
        <div className="flex gap-4">
          <Button
            type="button"
            variant="secondary"
            onClick={goToPreviousStep}
            className="py-2 border-primary text-primary"
          >
            <FaArrowLeft className="text-xl" size={16} />
            {t("previous", { ns: "translation" })}
          </Button>

          <Button
            className="bg-primary text-white py-2 border-none"
            type="button"
            onClick={goToNextStep}
            disabled={isNextButtonDisabled}
          >
            {t("next", { ns: "translation" })}
            <FaArrowRight className="text-xl" size={16} />
          </Button>
        </div>
      </div>
      <PublicAccessConfirmationModal
        opened={isPublicAccessConfirmationModalOpened}
        onClose={onCancelPublicAccess}
        onCancel={onCancelPublicAccess}
        onConfirm={onConfirmPublicAccess}
      />
    </>
  );
};
