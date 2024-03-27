import { Fragment } from "react";
import { Controller } from "react-hook-form";

import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { useAuthModes } from "@/lib/hooks/useAuthModes";

export const EmailInput = (): JSX.Element => {
  const { password, magicLink } = useAuthModes();
  if (!password && !magicLink) {
    return <Fragment />;
  }

  return (
    <Controller
      name="email"
      defaultValue=""
      render={({ field }) => (
        <TextInput
          label="Email"
          inputValue={field.value as string}
          setInputValue={field.onChange}
        />
      )}
    />
  );
};
