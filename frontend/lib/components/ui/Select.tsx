/*eslint complexity: ["error", 10]*/

/* eslint-disable max-lines */
import { BsCheckCircleFill } from "react-icons/bs";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/lib/components/ui/Popover";
import { cn } from "@/lib/utils";

export type SelectOptionProps<T> = {
  label: string;
  value: T;
};

type SelectProps<T> = {
  options: SelectOptionProps<T>[];
  value?: T;
  onChange: (option: T) => void;
  label?: string;
  readOnly?: boolean;
  className?: string;
  emptyLabel?: string;
  popoverClassName?: string;
  popoverSide?: "top" | "bottom" | "left" | "right" | undefined;
};

const selectedStyle = "rounded-lg bg-black text-white";

export const Select = <T extends string | number>({
  onChange,
  options,
  value,
  label,
  readOnly = false,
  className,
  emptyLabel,
  popoverClassName,
  popoverSide,
}: SelectProps<T>): JSX.Element => {
  const selectedValueLabel = options.find(
    (option) => option.value === value
  )?.label;

  if (readOnly) {
    return (
      <div className={cn("gap-2", className)}>
        {label !== undefined && (
          <label
            id="listbox-label"
            className="block text-sm font-medium leading-6 text-gray-900"
          >
            {label}
          </label>
        )}
        <div className="relative">
          <button
            type="button"
            className="relative w-full cursor-default rounded-md bg-white py-1.5 px-3 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 sm:text-sm sm:leading-6"
            aria-haspopup="listbox"
            disabled
          >
            <span className="flex items-center">
              <span className="mx-4 block truncate">
                {selectedValueLabel ?? emptyLabel ?? "-"}
              </span>
            </span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("gap-2", className)}>
      {label !== undefined && (
        <label
          id="listbox-label"
          className="block text-sm font-medium leading-6 text-gray-900"
        >
          {label}
        </label>
      )}
      <div className="relative">
        <Popover>
          <PopoverTrigger>
            <button
              type="button"
              className="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 sm:text-sm sm:leading-6"
              aria-haspopup="listbox"
            >
              <span className="flex items-center">
                <span className="ml-3 block truncate">
                  {selectedValueLabel ?? emptyLabel ?? "-"}
                </span>
              </span>
              <span className="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
                <svg
                  className="h-5 w-5 text-gray-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 3a.75.75 0 01.55.24l3.25 3.5a.75.75 0 11-1.1 1.02L10 4.852 7.3 7.76a.75.75 0 01-1.1-1.02l3.25-3.5A.75.75 0 0110 3zm-3.76 9.2a.75.75 0 011.06.04l2.7 2.908 2.7-2.908a.75.75 0 111.1 1.02l-3.25 3.5a.75.75 0 01-1.1 0l-3.25-3.5a.75.75 0 01.04-1.06z"
                    clipRule="evenodd"
                  />
                </svg>
              </span>
            </button>
          </PopoverTrigger>
          <PopoverContent
            className={cn("max-h-[200px] overflow-scroll", popoverClassName)}
            side={popoverSide ?? "top"}
          >
            <ul role="listbox">
              {options.map((option) => (
                <li
                  className="text-gray-900 relative cursor-pointer select-none py-0"
                  id="listbox-option-0"
                  key={option.value}
                  onClick={() => onChange(option.value)}
                >
                  <div
                    className={`flex items-center px-3 py-2 ${
                      value === option.value && selectedStyle
                    }`}
                  >
                    <span className="font-bold block truncate mr-2">
                      {option.label}
                    </span>
                    {value === option.value && <BsCheckCircleFill />}
                  </div>
                </li>
              ))}
            </ul>
          </PopoverContent>
        </Popover>
      </div>
    </div>
  );
};
