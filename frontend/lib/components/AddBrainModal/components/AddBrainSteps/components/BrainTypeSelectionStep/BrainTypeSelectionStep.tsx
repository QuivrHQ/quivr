import { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { FaArrowRight } from "react-icons/fa";

import Button from "@/lib/components/ui/Button";
import { Radio } from "@/lib/components/ui/Radio";

import { useBrainTypeSelectionStep } from "./hooks/useBrainTypeSelectionStep";
import { useKnowledgeSourceLabel } from "./hooks/useKnowledgeSourceLabel";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

type BrainTypeSelectionStepProps = {
  onCancelBrainCreation: () => void;
};

export const BrainTypeSelectionStep = ({
  onCancelBrainCreation,
}: BrainTypeSelectionStepProps): JSX.Element => {
  const { knowledgeSourceOptions } = useKnowledgeSourceLabel();
  const { register } = useBrainTypeSelectionStep();
  const { goToNextStep, currentStep } = useBrainCreationSteps();
  const { t } = useTranslation(["translation"]);
  if (currentStep !== "BRAIN_TYPE") {
    return <Fragment />;
  }

  return (
    <>
      <Radio
        items={knowledgeSourceOptions}
        className="flex-1 justify-between"
        {...register("brain_type")}
      />
      <div className="flex flex-row flex-1 justify-center w-full gap-48 mt-10">
        <Button
          type="button"
          variant="tertiary"
          onClick={onCancelBrainCreation}
        >
          {t("cancel")}
        </Button>

        <Button
          className="bg-primary text-white py-2 border-none"
          type="button"
          data-testid="create-brain-submit-button"
          onClick={goToNextStep}
        >
          {t("next")}
          <FaArrowRight className="text-xl" size={16} />
        </Button>
      </div>
    </>
  );
};
