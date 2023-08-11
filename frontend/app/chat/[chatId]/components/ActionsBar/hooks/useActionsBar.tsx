import { useState } from "react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useActionsBar = () => {
  const [value, setValue] = useState("");

  const handleChange = (newPlainTextValue: string) => {
    setValue(newPlainTextValue);
  };

  return {
    handleChange,
    value,
  };
};
