"use client";
import { ReactNode, forwardRef, useImperativeHandle, useState } from "react";
import * as ToastPrimitive from "@radix-ui/react-toast";
import Button from "./Button";
import { VariantProps, cva } from "class-variance-authority";
import { cn, generateUniqueId } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";

export interface ToastRef {
  publish: (toast: ToastContent) => void;
}

const ToastVariants = cva(
  "bg-white dark:bg-black px-8 max-w-sm w-full py-5 border border-black/10 dark:border-white/25 rounded-xl shadow-xl flex items-center pointer-events-auto data-[swipe=end]:opacity-0 data-[state=closed]:opacity-0 transition-opacity",
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

interface ToastContent extends VariantProps<typeof ToastVariants> {
  text: string;
  open?: boolean;
  id?: string;
}

interface ToastProps
  extends ToastPrimitive.ToastProps,
    VariantProps<typeof ToastVariants> {
  children?: ReactNode;
}

export const Toast = forwardRef(
  ({ children, variant, ...props }: ToastProps, forwardedRef) => {
    const [toasts, setToasts] = useState<ToastContent[]>([]);

    const toggleToast = (value: boolean, index: number) => {
      setToasts((toasts) =>
        toasts.map((toast, i) => {
          if (i === index) {
            toast.open = value;
          }
          return toast;
        })
      );
    };

    useImperativeHandle(
      forwardedRef,
      (): ToastRef => ({
        publish: (toast: ToastContent) => {
          setToasts((toasts) => {
            const newToasts = [...toasts];
            toast.open = true;
            toast.id = generateUniqueId();
            newToasts.push(toast);
            return newToasts;
          });
        },
      })
    );

    return (
      <>
        <AnimatePresence mode="popLayout">
          {toasts.map((toast, index) => {
            if (!toast.open) return;
            return (
              <ToastPrimitive.Root
                open={toast.open}
                onOpenChange={(value) => toggleToast(value, index)}
                asChild
                forceMount
                key={toast.id}
                {...props}
              >
                <motion.div
                  layout
                  initial={{ x: "100%", opacity: 0 }}
                  animate={{
                    x: "0%",
                    opacity: 1,
                  }}
                  exit={{ opacity: 0 }}
                  className={cn(ToastVariants({ variant: toast.variant }))}
                >
                  <ToastPrimitive.Description className="flex-1">
                    {toast.text}
                  </ToastPrimitive.Description>
                  <ToastPrimitive.Close asChild>
                    <Button variant={"tertiary"}>Dismiss</Button>
                  </ToastPrimitive.Close>
                </motion.div>
              </ToastPrimitive.Root>
            );
          })}
        </AnimatePresence>
        <ToastPrimitive.Viewport className="fixed flex-col bottom-0 left-0 right-0 p-5 flex items-end gap-2 outline-none pointer-events-none" />
      </>
    );
  }
);

export const ToastProvider = ({ children }: { children?: ReactNode }) => {
  return <ToastPrimitive.Provider>{children}</ToastPrimitive.Provider>;
};

Toast.displayName = "Toast";

export default Toast;
