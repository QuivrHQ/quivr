import { useState } from "react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useActionBar = () => {
  const [isUploading, setIsUploading] = useState(false);

  return {
    isUploading,
    setIsUploading,
  };
};
