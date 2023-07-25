import { Trigger } from "@radix-ui/react-tabs";

import { BrainManagementTab } from "../types";

type BrainTabTriggerProps = {
  label: string;
  value: BrainManagementTab;
  selected: boolean;
  onChange: (value: BrainManagementTab) => unknown;
};
export const BrainTabTrigger = ({
  label,
  value,
  selected,
  onChange,
}: BrainTabTriggerProps): JSX.Element => {
  return (
    <Trigger
      className={`tracking-wide flex-1 text-lg align-center ${
        selected ? "font-bold" : ""
      }`}
      value={value}
      onClick={() => onChange(value)}
    >
      {label}
    </Trigger>
  );
};
