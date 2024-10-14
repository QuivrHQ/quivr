"use client";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";

import styles from "./BooleansInputs.module.scss";

import { ConditionalInput } from "../../types/assistant";

interface BooleansInputsProps {
  booleans: { key: string; description: string }[];
  conditionalInputs?: ConditionalInput[];
  booleanStates: { [key: string]: boolean | null };
  setBooleanStates: React.Dispatch<
    React.SetStateAction<{ [key: string]: boolean | null }>
  >;
  selectTextStates: { [key: string]: string | null };
}

const BooleansInputs = ({
  booleans,
  conditionalInputs,
  booleanStates,
  setBooleanStates,
  selectTextStates,
}: BooleansInputsProps): JSX.Element => {
  const handleCheckboxChange = (key: string, checked: boolean) => {
    setBooleanStates((prevState: { [key: string]: boolean | null }) => ({
      ...prevState,
      [key]: checked,
    }));
  };

  const checkCondition = (conditionalInput: ConditionalInput): boolean => {
    const { key, condition, value } = conditionalInput;
    const targetValue =
      booleanStates[key]?.toString() ?? selectTextStates[key] ?? "";

    if (condition === "equals") {
      return targetValue === value;
    } else {
      return targetValue !== value;
    }
  };

  return (
    <div className={styles.boolean_inputs_wrapper}>
      {booleans.map((input, index) => {
        const shouldShow = !!conditionalInputs?.every((conditionalInput) => {
          if (conditionalInput.conditional_key === input.key) {
            return checkCondition(conditionalInput);
          }

          return true;
        });

        if (!shouldShow) {
          return null;
        }

        return (
          <div key={index} className={styles.boolean_input}>
            <Checkbox
              label={input.key}
              checked={!!booleanStates[input.key]}
              setChecked={(checked) => handleCheckboxChange(input.key, checked)}
            />
          </div>
        );
      })}
    </div>
  );
};

export default BooleansInputs;
