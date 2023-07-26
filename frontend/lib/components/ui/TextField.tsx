/* eslint-disable */
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
}

export const TextArea = forwardRef(
  ({ label, className, name, ...props }: FieldProps, forwardedRef) => {
    return (
      <fieldset className={cn("flex flex-col w-full", className)} name={name}>
        {label && (
          <label htmlFor={name} className="text-sm">
            {label}
          </label>
        )}
        <textarea
          ref={forwardedRef as RefObject<HTMLTextAreaElement>}
          className="w-full bg-gray-50 dark:bg-gray-900 px-4 py-2 border rounded-md border-black/10 dark:border-white/25"
          name={name}
          id={name}
          {...props}
        />
      </fieldset>
    );
  }
);
