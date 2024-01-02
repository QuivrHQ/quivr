import { Fragment } from "react";

import { cn } from "@/lib/utils";

import { Step } from "./components/Step";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const Stepper = (): JSX.Element => {
  const { currentStep, steps } = useBrainCreationSteps();

  return (
    <div className="flex flex-row justify-between w-full px-12 mb-12">
      {steps.map((step, index) => (
        <Fragment key={step.value}>
          <Step index={index} step={step} />
          {index < steps.length - 1 && ( // Add horizontal line for all but the last step
            <hr
              className={cn(
                "flex-grow border-t-2 border-primary m-4",
                step.value === currentStep
                  ? "border-primary"
                  : "border-gray-300"
              )}
            />
          )}
        </Fragment>
      ))}
    </div>
  );
};
