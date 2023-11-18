import { useEffect, useState } from "react";

import { useBrainFormState } from "../../../hooks/useBrainFormState";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAccessConfirmationModal = () => {
  const { dirtyFields, resetField, status } = useBrainFormState();
  const isStatusDirty = Boolean(dirtyFields.status);
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
