/* eslint-disable */
"use client";
import * as ToastPrimitive from "@radix-ui/react-toast";
import { AnimatePresence, motion } from "framer-motion";
import { ReactNode } from "react";
import { useTranslation } from "react-i18next";

import { cn } from "@/lib/utils";

import Button from "../../Button";
import { ToastContext } from "../domain/ToastContext";
import { ToastVariants } from "../domain/types";
import { useToastBuilder } from "../hooks/useToastBuilder";

export const Toast = ({
  children,
  ...toastProviderProps
}: {
  children?: ReactNode;
} & ToastPrimitive.ToastProviderProps): JSX.Element => {
  const { publish, toasts, toggleToast } = useToastBuilder();
  const { t } = useTranslation();

  return (
    <ToastPrimitive.Provider {...toastProviderProps}>
      <ToastContext.Provider value={{ publish }}>
        {children}
        <AnimatePresence mode="popLayout">
          {toasts.map((toast) => {
            if (toast.open !== true) {
              return;
            }

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
                      {t("toastDismiss")}
                    </Button>
                  </ToastPrimitive.Close>
                </motion.div>
              </ToastPrimitive.Root>
            );
          })}
        </AnimatePresence>
        <ToastPrimitive.Viewport className="fixed flex-col bottom-0 left-0 right-0 p-5 flex items-end gap-2 outline-none pointer-events-none z-[99999]" />
      </ToastContext.Provider>
    </ToastPrimitive.Provider>
  );
};

Toast.displayName = "Toast";
