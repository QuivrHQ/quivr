"use client";
import { ReactNode, forwardRef, useImperativeHandle, useState } from "react";
import * as ToastPrimitive from "@radix-ui/react-toast";
import Button from "./Button";
import { VariantProps, cva } from "class-variance-authority";
import { cn } from "@/lib/utils";

export interface ToastRef {
  publish: () => void;
}

const ToastVariants = cva(
  "bg-white dark:bg-black px-8 max-w-sm w-full py-5 border border-black/10 dark:border-white/25 rounded-xl shadow-xl flex items-center pointer-events-auto",
  {
    variants: {
      variant: {
        neutral: "",
        danger: "bg-red-400 dark:bg-red-600",
        success: "bg-green-400 dark:bg-green-600",
      },
    },
    defaultVariants: {
      variant: "neutral",
    },
  }
);

interface ToastProps
  extends ToastPrimitive.ToastProps,
    VariantProps<typeof ToastVariants> {
  children?: ReactNode;
}

export const Toast = forwardRef(
  ({ children, variant, ...props }: ToastProps, forwardedRef) => {
    const [count, setCount] = useState(0);

    useImperativeHandle(forwardedRef, () => ({
      publish: () => setCount((count) => count + 1),
    }));

    return (
      <>
        {Array.from({ length: count }).map((_, index) => (
          <ToastPrimitive.Root
            className={cn(ToastVariants({ variant }))}
            key={index}
            {...props}
          >
            <ToastPrimitive.Description className="flex-1">
              {children}
            </ToastPrimitive.Description>
            <ToastPrimitive.Close asChild>
              <Button variant={"tertiary"}>Dismiss</Button>
            </ToastPrimitive.Close>
          </ToastPrimitive.Root>
        ))}
        <ToastPrimitive.Viewport className="fixed flex-col bottom-0 left-0 right-0 p-5 flex items-end gap-2 outline-none pointer-events-none" />
      </>
    );
  }
);

export const ToastProvider = ({ children }: { children?: ReactNode }) => {
  return <ToastPrimitive.Provider>{children}</ToastPrimitive.Provider>;
};

export default Toast;
