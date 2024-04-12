import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { Step } from "@/lib/types/Modal";

import { useBrainCreationContext } from "../brainCreation-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainCreationSteps = () => {
  const { t } = useTranslation("brain");
  const { isBrainCreationModalOpened, currentStep, setCurrentStep } =
    useBrainCreationContext();

  const steps: Step[] = [
    {
      label: t("brain_type"),
      value: "FIRST_STEP",
    },
    {
      label: t("brain_params"),
      value: "SECOND_STEP",
    },
    {
      label: t("resources"),
      value: "THIRD_STEP",
    },
  ];

  const currentStepIndex = steps.findIndex(
    (step) => step.value === currentStep
  );

  useEffect(() => {
    goToFirstStep();
  }, [isBrainCreationModalOpened]);

  const goToNextStep = () => {
    if (currentStepIndex === -1 || currentStepIndex === steps.length - 1) {
      return;
    }
    const nextStep = steps[currentStepIndex + 1];

    return setCurrentStep(nextStep.value);
  };

  const goToPreviousStep = () => {
    if (currentStepIndex === -1 || currentStepIndex === 0) {
      return;
    }
    const previousStep = steps[currentStepIndex - 1];

    return setCurrentStep(previousStep.value);
  };

  const goToFirstStep = () => {
    return setCurrentStep(steps[0].value);
  };

  return {
    currentStep,
    steps,
    goToNextStep,
    goToPreviousStep,
    currentStepIndex,
  };
};
