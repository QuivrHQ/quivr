import { useContext } from "react";
import { ToastContext } from "../components/ui/Toast/domain/ToastContext";

export const useToast = () => {
  const { publish } = useContext(ToastContext);

  return {
    publish,
  };
};
