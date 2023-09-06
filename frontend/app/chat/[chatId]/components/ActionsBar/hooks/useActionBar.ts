import { useState } from "react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useActionBar = () => {
  const [shouldDisplayUploadCard, setShouldDisplayUploadCard] = useState(false);

  return {
    shouldDisplayUploadCard,
    setShouldDisplayUploadCard,
  };
};
