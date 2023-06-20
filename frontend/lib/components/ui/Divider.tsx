/* eslint-disable */
import { forwardRef, HTMLAttributes, LegacyRef } from "react";

import { cn } from "@/lib/utils";

type DividerProps = HTMLAttributes<HTMLDivElement> & {
  text?: string;
};

const Divider = forwardRef(
  ({ className, text, ...props }: DividerProps, ref): JSX.Element => {
    return (
      <div
        ref={ref as LegacyRef<HTMLDivElement>}
        className={cn("flex items-center justify-center", className)}
        {...props}
      >
        <hr className="border-t border-gray-300 w-12" />
        {text !== undefined && (
          <p className="px-3 text-center text-gray-500 dark:text-white">
            {text}
          </p>
        )}
        <hr className="border-t border-gray-300 w-12" />
      </div>
    );
  }
);
Divider.displayName = "AnimatedCard";

export { Divider };
