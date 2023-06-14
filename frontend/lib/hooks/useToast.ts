import { ToastContext } from "@/lib/components/ui/Toast/domain/ToastContext";
import { useContext } from "react";

export const useToast = () => {
  const { publish } = useContext(ToastContext);

  return {
    publish,
  };
};
