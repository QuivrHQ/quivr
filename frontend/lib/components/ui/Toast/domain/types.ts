import { cva, VariantProps } from "class-variance-authority";

export const ToastVariants = cva(
  "bg-white dark:bg-black px-8 max-w-sm w-full py-5 border border-black/10 dark:border-white/25 rounded-xl shadow-xl flex items-center pointer-events-auto data-[swipe=end]:opacity-0 data-[state=closed]:opacity-0 transition-opacity",
  {
    variants: {
      variant: {
        neutral: "bg-gray-500 dark:bg-gray-600",
        danger: "bg-red-500 text-white dark:bg-red-600",
        success: "bg-green-500 text-white dark:bg-green-600",
        warning: "bg-orange-500 text-white dark:bg-orange-600",
      },
    },
    defaultVariants: {
      variant: "neutral",
    },
  }
);

type ToastVariant = NonNullable<VariantProps<typeof ToastVariants>["variant"]>;

export interface ToastData {
  text: string;
  variant: ToastVariant;
}

export interface ToastContent extends ToastData {
  open?: boolean;
  id: string;
}

export type ToastPublisher = (toast: ToastData) => void;
