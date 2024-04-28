import React from "react";

import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./Stepper.module.scss";

import { StepValue } from "../../types/types";

interface StepperProps {
  currentStep: StepValue;
  steps: { value: string; label: string }[];
}

export const Stepper = ({ currentStep, steps }: StepperProps): JSX.Element => {
  const currentStepIndex = steps.findIndex(
    (step) => step.value === currentStep
  );

  return (
    <div className={styles.stepper_wrapper}>
      {steps.map((step, index) => (
        <React.Fragment key={step.value}>
          <div
            className={`${styles.step} ${
              index === currentStepIndex
                ? styles.current_step
                : index < currentStepIndex
                ? styles.done_step
                : styles.pending_step
            }`}
            key={step.value}
          >
            <div className={styles.circle}>
              <div className={styles.inside_circle}>
                {index < currentStepIndex && (
                  <Icon name="check" size="normal" color="white" />
                )}
              </div>
            </div>
            <div className={styles.step_info}>
              <span className={styles.step_index}>STEP {index + 1}</span>
              <span className={styles.step_status}>
                {index === currentStepIndex
                  ? "Progress"
                  : index < currentStepIndex
                  ? "Completed"
                  : "Pending"}
              </span>
            </div>
          </div>
          {index < steps.length - 1 && (
            <div
              className={`
              ${styles.bar} 
              ${index < currentStepIndex ? styles.done : ""}
              `}
            ></div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
};
