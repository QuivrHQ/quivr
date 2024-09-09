import { Controller } from "react-hook-form";

import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";

import styles from "./Prompt.module.scss";

export const Prompt = (): JSX.Element => {
  return (
    <div className={styles.prompt_wrapper}>
      <div>
        <FieldHeader label="Instructions" iconName="paragraph" />
        <Controller
          name="prompt.content"
          defaultValue=""
          render={({ field }) => (
            <TextAreaInput
              label="Write specific instructions for your brain here"
              inputValue={field.value as string}
              setInputValue={field.onChange}
            />
          )}
        />
      </div>
    </div>
  );
};
