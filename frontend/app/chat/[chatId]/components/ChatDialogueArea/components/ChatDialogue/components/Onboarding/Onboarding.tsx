import { useState } from "react";

import { Step1 } from "./components";
import { Step2 } from "./components/Step2";
import { OnboardingState } from "../types";

export const Onboarding = (): JSX.Element => {
  const [currentStep, setCurrentStep] = useState<OnboardingState>("DOWNLOAD");

  return (
    <div className="flex flex-col gap-2">
      <Step1 changeStateTo={setCurrentStep} currentStep={currentStep} />
      <Step2 currentStep={currentStep} />
    </div>
  );
};
