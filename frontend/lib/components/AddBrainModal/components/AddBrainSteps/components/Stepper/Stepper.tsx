import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./Stepper.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const Stepper = (): JSX.Element => {
  const { currentStep, steps } = useBrainCreationSteps();

  const currentStepIndex =
    steps.findIndex((step) => step.value === currentStep) + 1;

  return (
    <div className={styles.stepper_wrapper}>
      {steps.map((step, index) => (
        <>
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
            <div className={styles.step_info}>Heyeyuyiuye</div>
          </div>
          {index < steps.length - 1 && (
            <div
              className={`
              ${styles.bar} 
              ${index < currentStepIndex ? styles.done : ""}
              `}
            ></div>
          )}
        </>
      ))}
    </div>
  );
};
