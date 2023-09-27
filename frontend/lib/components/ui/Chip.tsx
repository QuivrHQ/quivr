import { HTMLProps } from "react";

import { cn } from "@/lib/utils";

export const Chip = ({
  label,
  children,
  className,
  ...restProps
}: HTMLProps<HTMLSpanElement>): JSX.Element => {
  return (
    <span
      className={cn(
        "px-2 bg-gray-400 text-black rounded-xl text-sm flex items-center justify-center",
        className
      )}
      {...restProps}
    >
      {label ?? children}
    </span>
  );
};
