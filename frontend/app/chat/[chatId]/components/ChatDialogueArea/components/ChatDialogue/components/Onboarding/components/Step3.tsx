import { Fragment } from "react";

import { useOnboardingContext } from "@/lib/hooks/useOnboardingContext";

import { checkIfShouldDisplayStep } from "../helpers/checkIfShouldDisplayStep";

export const Step3 = (): JSX.Element => {
  const { currentStep } = useOnboardingContext();
  const shouldStepBeDisplayed = checkIfShouldDisplayStep({
    currentStep,
    step: "UPLOADED",
  });

  if (!shouldStepBeDisplayed) {
    return <Fragment />;
  }

  return <p>hello</p>;
};
