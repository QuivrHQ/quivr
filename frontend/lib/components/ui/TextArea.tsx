import {
  DetailedHTMLProps,
  forwardRef,
  InputHTMLAttributes,
  RefObject,
} from "react";

import { cn } from "@/lib/utils";

interface FieldProps
  extends DetailedHTMLProps<
    InputHTMLAttributes<HTMLTextAreaElement>,
    HTMLTextAreaElement
  > {
  label?: string;
  name: string;
  inputClassName?: string;
}

export const TextArea = forwardRef(
  (
    {
      label,
      className,
      inputClassName,
      name,
      required = false,
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
        <textarea
          ref={forwardedRef as RefObject<HTMLTextAreaElement>}
          className={cn(
            "w-full bg-gray-50 dark:bg-gray-900 px-4 py-2 border rounded-md border-black/10 dark:border-white/25",
            inputClassName
          )}
          name={name}
          id={name}
          {...props}
        />
      </fieldset>
    );
  }
);

TextArea.displayName = "TextArea";
