import { FaCheckCircle } from "react-icons/fa";

import { cn } from "@/lib/utils";

import { useBrainCreationSteps } from "../../../hooks/useBrainCreationSteps";
import { Step as StepType } from "../../../types";

type StepProps = {
  index: number;
  step: StepType;
};

export const Step = ({ index, step }: StepProps): JSX.Element => {
  const { currentStep, currentStepIndex } = useBrainCreationSteps();
  const isStepDone = index < currentStepIndex;
  const stepContent = isStepDone ? <FaCheckCircle /> : index + 1;

  return (
    <div
      key={step.label}
      className="flex flex-row justify-center items-center flex-1"
    >
      <div className="flex flex-col justify-center items-center">
        <div
          className={cn(
            "h-[40px] w-[40px] border-solid rounded-full flex flex-row items-center justify-center mb-2 border-primary border-2 text-primary",
            isStepDone ? "bg-primary text-white" : "",
            step.value === currentStep ? "bg-primary text-white" : ""
          )}
        >
          {stepContent}
        </div>
        <span key={step.label} className="text-xs text-center">
          {step.label}
        </span>
      </div>
    </div>
  );
};
