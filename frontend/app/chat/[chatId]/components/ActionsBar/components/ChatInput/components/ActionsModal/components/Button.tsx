import { forwardRef } from "react";

import CoreButton, {
  ButtonProps as CoreButtonProps,
} from "@/lib/components/ui/Button";
import { cn } from "@/lib/utils";

type ButtonProps = CoreButtonProps & {
  onClick?: () => void;
  className?: string;
  label?: string;
  startIcon?: JSX.Element;
  endIcon?: JSX.Element;
};

export const Button = forwardRef(
  (
    { onClick, className, label, startIcon, endIcon, ...props }: ButtonProps,
    forwardedRef
  ): JSX.Element => {
    return (
      <CoreButton
        className={cn("p-2 sm:px-3 text-primary focus:ring-0", className)}
        variant={"tertiary"}
        data-testid="config-button"
        ref={forwardedRef}
        onClick={onClick}
        {...props}
      >
        <div className="flex flex-row justify-between w-full items-center">
          <div className="flex flex-row gap-2 items-center">
            {startIcon}
            <span className="hidden sm:block">{label}</span>
          </div>
          {endIcon}
        </div>
      </CoreButton>
    );
  }
);

Button.displayName = CoreButton.displayName;
