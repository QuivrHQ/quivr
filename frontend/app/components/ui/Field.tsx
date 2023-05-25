import { cn } from "@/lib/utils";
import { DetailedHTMLProps, FC, InputHTMLAttributes } from "react";

interface FieldProps
  extends DetailedHTMLProps<
    InputHTMLAttributes<HTMLInputElement>,
    HTMLInputElement
  > {
  label?: string;
  name: string;
}

const Field: FC<FieldProps> = ({ label, className, name, id, ...props }) => {
  return (
    <fieldset className={cn("flex flex-col w-full", className)} name={name}>
      {label && (
        <label htmlFor={name} className="text-sm">
          {label}
        </label>
      )}
      <input
        className="w-full bg-gray-50 dark:bg-gray-900 px-4 py-2 border rounded-md border-black/10 dark:border-white/25"
        name={name}
        id={name}
        {...props}
      />
    </fieldset>
  );
};

export default Field;
