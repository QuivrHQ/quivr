import { cn } from "@/lib/utils";
import { FC, HTMLAttributes, LegacyRef, forwardRef } from "react";

type DividerProps = HTMLAttributes<HTMLDivElement> & {
  text?: string;
};

const Divider: FC<DividerProps> = forwardRef(
  ({ className, text, ...props }, ref) => {
    return (
      <div
        ref={ref as LegacyRef<HTMLDivElement>}
        className={cn("flex items-center justify-center", className)}
        {...props}
      >
        <hr className="border-t border-gray-300 w-12" />
        {text !== undefined && (
          <p className="px-3 bg-white text-center text-gray-500">{text}</p>
        )}
        <hr className="border-t border-gray-300 w-12" />
      </div>
    );
  }
);
Divider.displayName = "AnimatedCard";

export { Divider };
