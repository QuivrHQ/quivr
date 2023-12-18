import {
  DetailedHTMLProps,
  forwardRef,
  InputHTMLAttributes,
  RefObject,
} from "react";

import { cn } from "@/lib/utils";

interface FieldProps
  extends DetailedHTMLProps<
    InputHTMLAttributes<HTMLInputElement>,
    HTMLInputElement
  > {
  label?: string;
  name: string;
  icon?: React.ReactNode;
  inputClassName?: string;
}

const Field = forwardRef(
  (
    {
      label,
      className,
      name,
      inputClassName,
      required = false,
      icon,
      ...props
    }: FieldProps,
    forwardedRef
  ) => {
    return (
      <fieldset className={cn("flex flex-col w-full", className)} name={name}>
        {label !== undefined && (
          <label htmlFor={name} className="text-sm font-semibold mb-2">
            {label}
            {required && <span>*</span>}
          </label>
        )}
        <div className="relative">
          <input
            ref={forwardedRef as RefObject<HTMLInputElement>}
            className={cn(
              `w-full bg-gray-50 dark:bg-gray-900 px-4 py-2 border rounded-md border-black/10 dark:border-white/25`,
              icon !== undefined ? "pr-12" : "",
              inputClassName
            )}
            name={name}
            id={name}
            {...props}
          />
          {icon !== undefined && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              {icon}
            </div>
          )}
        </div>
      </fieldset>
    );
  }
);
Field.displayName = "Field";

export default Field;
