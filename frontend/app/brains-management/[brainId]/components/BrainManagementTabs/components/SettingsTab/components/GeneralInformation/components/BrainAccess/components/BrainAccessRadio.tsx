import { IconType } from "react-icons/lib";

import { cn } from "@/lib/utils";

type BrainAccessRadioProps = {
  onSelect: () => void;
  label: string;
  description: string;
  Icon: IconType;
  isSelected: boolean;
};

export const BrainAccessRadio = ({
  onSelect,
  description,
  label,
  Icon,
  isSelected,
}: BrainAccessRadioProps): JSX.Element => {
  return (
    <div
      className={cn(
        "flex flex-row justify-center bg-white rounded-md gap-2 p-5 cursor-pointer items-center border-2 border-white",
        isSelected ? "border-primary" : ""
      )}
      onClick={onSelect}
    >
      <Icon className="text-primary" size={30} />
      <div className="flex flex-1 flex-col">
        <span className="font-semibold">{label}</span>
        <span>{description}</span>
      </div>
    </div>
  );
};
