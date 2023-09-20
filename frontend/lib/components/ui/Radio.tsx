import { DetailedHTMLProps, forwardRef, InputHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type RadioItem = {
  value: string;
  label: string;
};

interface RadioProps
  extends DetailedHTMLProps<
    InputHTMLAttributes<HTMLInputElement>,
    HTMLInputElement
  > {
  name: string;
  items: RadioItem[];
  label?: string;
  className?: string;
}

export const Radio = forwardRef<HTMLInputElement, RadioProps>(
  ({ items, label, className, value, ...props }, ref) => (
    <div className={cn("flex flex-col", className)}>
      {label !== undefined && (
        <label className="text-sm font-medium leading-6 mb-2">{label}</label>
      )}
      <div className="flex flex-row gap-4">
        {items.map((item) => (
          <div key={item.value} className="flex items-center mb-2">
            <input
              ref={ref} // Forward the ref to the input element
              type="radio"
              className="form-radio h-4 w-4 text-indigo-600 border-indigo-600"
              value={item.value}
              checked={value === item.value}
              {...props}
            />
            <label className="ml-2" htmlFor={item.value}>
              {item.label}
            </label>
          </div>
        ))}
      </div>
    </div>
  )
);

Radio.displayName = "Radio";
