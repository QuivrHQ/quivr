import { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { FaArrowLeft } from "react-icons/fa";

import { ApiRequestDefinition } from "@/lib/components/ApiRequestDefinition";
import Button from "@/lib/components/ui/Button";
import { BrainType } from "@/lib/types/brainConfig";

import { CompositeBrainConnections } from "./components/CompositeBrainConnections/CompositeBrainConnections";
import { KnowledgeToFeedInput } from "./components/KnowledgeToFeedInput";
import { useBrainCreationHandler } from "./hooks/useBrainCreationHandler";
import { useBrainKnowledgeStep } from "./hooks/useBrainKnowledgeStep";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

type BrainKnowledgeStepProps = {
  onCancelBrainCreation: () => void;
};

export const BrainKnowledgeStep = ({
  onCancelBrainCreation,
}: BrainKnowledgeStepProps): JSX.Element => {
  const { brainType, isSubmitButtonDisabled } = useBrainKnowledgeStep();
  const { t } = useTranslation(["translation"]);
  const { goToPreviousStep, currentStep } = useBrainCreationSteps();
  const { handleCreateBrain, isBrainCreationPending } = useBrainCreationHandler(
    {
      closeBrainCreationModal: onCancelBrainCreation,
    }
  );

  const brainTypeToKnowledgeComponent: Record<BrainType, JSX.Element> = {
    doc: <KnowledgeToFeedInput />,
    api: <ApiRequestDefinition />,
    composite: <CompositeBrainConnections />,
  };

  if (currentStep !== "KNOWLEDGE" || brainType === undefined) {
    return <Fragment />;
  }

  return (
    <>
      {brainTypeToKnowledgeComponent[brainType]}
      <div className="flex flex-row justify-between items-center flex-1 mt-10 w-full">
        <Button
          type="button"
          variant="tertiary"
          onClick={onCancelBrainCreation}
          className="text-primary"
          disabled={isBrainCreationPending}
        >
          {t("cancel", { ns: "translation" })}
        </Button>
        <div className="flex gap-4">
          <Button
            type="button"
            variant="secondary"
            onClick={goToPreviousStep}
            className="py-2 border-primary text-primary"
            disabled={isBrainCreationPending}
          >
            <FaArrowLeft className="text-xl" size={16} />
            {t("previous", { ns: "translation" })}
          </Button>

          <Button
            className="bg-primary text-white py-2 border-none"
            type="button"
            onClick={() => void handleCreateBrain()}
            disabled={isSubmitButtonDisabled || isBrainCreationPending}
            isLoading={isBrainCreationPending}
          >
            {t("createButton", { ns: "translation" })}
          </Button>
        </div>
      </div>
    </>
  );
};
