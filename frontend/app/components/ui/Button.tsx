import { ButtonHTMLAttributes, FC } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const ButtonVariants = cva(
  "px-8 py-3 text-sm font-medium rounded-md focus:ring ring-primary/10 outline-none flex items-center gap-2 disabled:opacity-50 transition-opacity",
  {
    variants: {
      variant: {
        primary:
          "bg-black text-white dark:bg-white dark:text-black hover:bg-gray-700 dark:hover:bg-gray-200 transition-colors",
        tertiary: "text-black dark:text-white bg-transparent py-2 px-4",
        secondary:
          "border border-black dark:border-white bg-white dark:bg-black text-black dark:text-white focus:bg-black dark:focus:bg-white hover:bg-black dark:hover:bg-white hover:text-white dark:hover:text-black focus:text-white transition-colors py-2 px-4 shadow-none",
      },
      brightness: {
        dim: "",
        default: "",
      },
    },
    defaultVariants: {
      variant: "primary",
      brightness: "default",
    },
  }
);
export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof ButtonVariants> {
  isLoading?: boolean;
}

const Button: FC<ButtonProps> = ({
  className,
  children,
  variant,
  brightness,
  ...props
}) => {
  return (
    <button
      className={cn(ButtonVariants({ variant, brightness, className }))}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
