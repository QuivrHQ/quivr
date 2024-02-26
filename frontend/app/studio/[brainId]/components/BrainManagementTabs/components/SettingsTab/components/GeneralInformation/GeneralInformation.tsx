/* eslint max-lines:["error", 150] */

import { Controller } from "react-hook-form";

import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

type GeneralInformationProps = {
  hasEditRights: boolean;
};

export const GeneralInformation = (
  props: GeneralInformationProps
): JSX.Element => {
  const { hasEditRights } = props;

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 justify-between w-full items-end">
        <Controller
          name="name"
          render={({ field }) => (
            <TextInput
              label="Name"
              inputValue={field.value as string}
              setInputValue={field.onChange}
              disabled={!hasEditRights}
            />
          )}
        />

        <Controller
          name="description"
          render={({ field }) => (
            <TextAreaInput
              label="Description"
              inputValue={field.value as string}
              setInputValue={field.onChange}
              disabled={!hasEditRights}
            />
          )}
        />
      </div>
    </>
  );
};
