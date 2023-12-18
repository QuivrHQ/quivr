/* eslint-disable */
import { forwardRef, HTMLAttributes, LegacyRef } from "react";

import { cn } from "@/lib/utils";

type DividerProps = HTMLAttributes<HTMLDivElement> & {
  text?: string;
  textClassName?: string;
  separatorClassName?: string;
};

const Divider = forwardRef(
  (
    {
      className,
      separatorClassName,
      textClassName,
      text,
      ...props
    }: DividerProps,
    ref
  ): JSX.Element => {
    return (
      <div
        ref={ref as LegacyRef<HTMLDivElement>}
        className={cn("flex items-center justify-center", className)}
        {...props}
      >
        <hr
          className={cn("border-t border-gray-300 w-12", separatorClassName)}
        />
        {text !== undefined && (
          <p
            className={cn(
              "px-3 text-center text-gray-500 dark:text-white",
              textClassName
            )}
          >
            {text}
          </p>
        )}
        <hr
          className={cn("border-t border-gray-300 w-12", separatorClassName)}
        />
      </div>
    );
  }
);
Divider.displayName = "AnimatedCard";

export { Divider };
