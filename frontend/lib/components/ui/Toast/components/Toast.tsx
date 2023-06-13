"use client";
import { cn } from "@/lib/utils";
import * as ToastPrimitive from "@radix-ui/react-toast";
import { AnimatePresence, motion } from "framer-motion";
import { ReactNode } from "react";
import Button from "../../Button";
import { ToastContext } from "../domain/ToastContext";
import { ToastVariants } from "../domain/types";
import { useToastBuilder } from "../hooks/useToastBuilder";

export const Toast = ({
  children,
  ...toastProviderProps
}: { children?: ReactNode } & ToastPrimitive.ToastProviderProps) => {
  const { publish, toasts, toggleToast } = useToastBuilder();
  return (
    <ToastPrimitive.Provider {...toastProviderProps}>
      <ToastContext.Provider value={{ publish }}>
        {children}
        <AnimatePresence mode="popLayout">
          {toasts.map((toast) => {
            if (!toast.open) return;
            return (
              <ToastPrimitive.Root
                open={toast.open}
                onOpenChange={(value) => toggleToast(value, toast.id)}
                asChild
                forceMount
                key={toast.id}
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
                    <Button variant={"tertiary"} className="text-white">
                      Dismiss
                    </Button>
                  </ToastPrimitive.Close>
                </motion.div>
              </ToastPrimitive.Root>
            );
          })}
        </AnimatePresence>
        <ToastPrimitive.Viewport className="fixed flex-col bottom-0 left-0 right-0 p-5 flex items-end gap-2 outline-none pointer-events-none" />
      </ToastContext.Provider>
    </ToastPrimitive.Provider>
  );
};

Toast.displayName = "Toast";
