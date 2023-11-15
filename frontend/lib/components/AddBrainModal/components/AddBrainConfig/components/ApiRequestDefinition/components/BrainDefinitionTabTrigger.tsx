import { Trigger } from "@radix-ui/react-tabs";

import { ApiTab } from "../types";

type BrainDefinitionTabTriggerProps = {
  label: string;
  value: ApiTab;
  selected: boolean;
  onChange: (value: ApiTab) => unknown;
};

export const BrainDefinitionTabTrigger = ({
  label,
  value,
  selected,
  onChange,
}: BrainDefinitionTabTriggerProps): JSX.Element => {
  return (
    <Trigger
      className={`flex-1 pb-2 border-gray-500 text-md align-center mb-0 ${
        selected ? "font-medium border-b-2" : ""
      }`}
      value={value}
      onClick={() => onChange(value)}
    >
      {label}
    </Trigger>
  );
};
