import { useState } from "react";

import { Step1 } from "./components";
import { OnboardingState } from "../types";

export const Onboarding = (): JSX.Element => {
  const [currentStep] = useState<OnboardingState>("DOWNLOAD");

  return (
    <div className="flex flex-col gap-2">
      <Step1 currentStep={currentStep} />
    </div>
  );
};
