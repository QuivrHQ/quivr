import { useContext } from "react";

import { ToastContext } from "../components/ui/Toast/domain/ToastContext";
import { ToastPublisher } from "../components/ui/Toast/domain/types";

export const useToast = (): { publish: ToastPublisher, setTop: () => void } => {
    const { publish, setTop } = useContext(ToastContext);

  return {
      publish,
      setTop,
  };
};
