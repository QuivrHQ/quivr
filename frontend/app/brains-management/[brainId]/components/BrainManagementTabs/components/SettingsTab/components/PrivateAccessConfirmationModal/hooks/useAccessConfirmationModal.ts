import { useEffect, useState } from "react";
import { UseFormResetField } from "react-hook-form";

import { BrainConfig, BrainStatus } from "@/lib/types/brainConfig";

type UseAccessConfirmationModalProps = {
  status: BrainStatus;
  setValue: (name: "status", value: "private" | "public") => void;
  isStatusDirty: boolean;
  resetField: UseFormResetField<BrainConfig>;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAccessConfirmationModal = ({
  status,
  isStatusDirty,
  resetField,
}: UseAccessConfirmationModalProps) => {
  const [isAccessModalOpened, setIsAccessModalOpened] = useState(false);

  useEffect(() => {
    if (!isStatusDirty) {
      return;
    }
    setIsAccessModalOpened(true);
  }, [isStatusDirty, status]);

  const closeModal = () => {
    setIsAccessModalOpened(false);
  };

  const onCancel = () => {
    closeModal();
    resetField("status", {
      defaultValue: status === "private" ? "public" : "private",
    });
  };

  return {
    isAccessModalOpened,
    closeModal,
    onCancel,
  };
};
