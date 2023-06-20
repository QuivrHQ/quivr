import { useContext } from "react";

import { ToastContext } from "../components/ui/Toast/domain/ToastContext";
import { ToastPublisher } from "../components/ui/Toast/domain/types";

export const useToast = (): { publish: ToastPublisher } => {
  const { publish } = useContext(ToastContext);

  return {
    publish,
  };
};
