/* eslint-disable */
import { useContext } from "react";

import { ToastContext } from "@/lib/components/ui/Toast/domain/ToastContext";

export const useToast = () => {
  const { publish } = useContext(ToastContext);

  return {
    publish,
  };
};
