import { useEffect, useState } from "react";
import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePublicAccessConfirmationModal = () => {
  const {
    watch,
    setValue,
    formState: { dirtyFields },
  } = useFormContext<CreateBrainProps>();

  const [
    isPublicAccessConfirmationModalOpened,
    setIsPublicAccessConfirmationModalOpened,
  ] = useState(false);

  const status = watch("status");

  useEffect(() => {
    if (status === "public" && dirtyFields.status === true) {
      setIsPublicAccessConfirmationModalOpened(true);
    }
  }, [dirtyFields.status, status]);

  const onConfirmPublicAccess = () => {
    setIsPublicAccessConfirmationModalOpened(false);
  };

  const onCancelPublicAccess = () => {
    setValue("status", "private", {
      shouldDirty: true,
    });
    setIsPublicAccessConfirmationModalOpened(false);
  };

  return {
    isPublicAccessConfirmationModalOpened,
    onConfirmPublicAccess,
    onCancelPublicAccess,
  };
};
