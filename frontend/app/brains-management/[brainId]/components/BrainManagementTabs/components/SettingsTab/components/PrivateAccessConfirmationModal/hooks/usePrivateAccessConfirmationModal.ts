import { useEffect, useState } from "react";

import { BrainStatus } from "@/lib/types/brainConfig";

type UsePrivateAccessModalProps = {
  status: BrainStatus;
  setValue: (name: "status", value: "private" | "public") => void;
  isStatusDirty: boolean;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePrivateAccessConfirmationModal = ({
  status,
  setValue,
  isStatusDirty,
}: UsePrivateAccessModalProps) => {
  const [isPrivateAccessModalOpened, setIsPrivateAccessModalOpened] =
    useState(false);

  useEffect(() => {
    if (status === "private" && isStatusDirty) {
      setIsPrivateAccessModalOpened(true);
    }
  }, [status]);

  const closeModal = () => {
    setIsPrivateAccessModalOpened(false);
  };

  const onCancel = () => {
    closeModal();
    setValue("status", "public");
  };

  return {
    isPrivateAccessModalOpened,
    closeModal,
    onCancel,
  };
};
