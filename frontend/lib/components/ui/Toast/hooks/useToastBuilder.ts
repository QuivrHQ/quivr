/* eslint-disable */
import { useState } from "react";

import { ToastContent, ToastData, ToastPublisher } from "../domain/types";
import { generateToastUniqueId } from "../helpers/generateToastUniqueId";

// ⚠️ You should not probably import this. use `useToast` instead
export const useToastBuilder = () => {
  const [toasts, setToasts] = useState<ToastContent[]>([]);

  const toggleToast = (value: boolean, toastId: string) => {
    setToasts((toasts) =>
      toasts.map((toast) => {
        if (toast.id === toastId) {
          toast.open = value;
        }

        return toast;
      })
    );
  };

  const publish: ToastPublisher = (newTost: ToastData) => {
    setToasts((toasts) => [
      ...toasts,
      { ...newTost, open: true, id: generateToastUniqueId() },
    ]);
  };

  return {
    publish,
    toggleToast,
    toasts,
  };
};
