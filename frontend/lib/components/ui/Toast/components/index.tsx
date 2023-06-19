"use client";
import * as ToastPrimitive from "@radix-ui/react-toast";
import { ReactNode } from "react";

import { Toast } from "./Toast";

export const ToastProvider = ({
  children,
  ...toastProviderProps
}: {
  children?: ReactNode;
} & ToastPrimitive.ToastProviderProps): JSX.Element => {
  return <Toast {...toastProviderProps}>{children}</Toast>;
};
