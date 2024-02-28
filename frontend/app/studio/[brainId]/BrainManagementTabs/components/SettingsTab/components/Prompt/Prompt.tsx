import { Controller } from "react-hook-form";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./Prompt.module.scss";

import { usePrompt, UsePromptProps } from "../../hooks/usePrompt";
import { PublicPrompts } from "../PublicPrompts/PublicPrompts";

type PromptProps = {
  usePromptProps: UsePromptProps;
  isUpdatingBrain: boolean;
};

export const Prompt = (props: PromptProps): JSX.Element => {
  const { isUpdatingBrain, usePromptProps } = props;

  const {
    pickPublicPrompt,
    submitPrompt,
    promptId,
    isRemovingPrompt,
    removeBrainPrompt,
  } = usePrompt(usePromptProps);

  return (
    <div className={styles.prompt_wrapper}>
      <PublicPrompts onSelect={pickPublicPrompt} />
      <Controller
        name="promptName"
        defaultValue=""
        render={({ field }) => (
          <TextInput
            label="Prompt Name"
            inputValue={field.value as string}
            setInputValue={field.onChange}
          />
        )}
      />
      <Controller
        name="promptContent"
        defaultValue=""
        render={({ field }) => (
          <TextAreaInput
            label="Prompt Content"
            inputValue={field.value as string}
            setInputValue={field.onChange}
          />
        )}
      />
      <div className={styles.buttons_wrapper}>
        {promptId !== "" && (
          <QuivrButton
            disabled={isUpdatingBrain || isRemovingPrompt}
            onClick={() => void removeBrainPrompt()}
            label="Remove Prompt"
            color="dangerous"
            iconName="delete"
          ></QuivrButton>
        )}
        <div>
          <QuivrButton
            label="Save"
            iconName="upload"
            color="primary"
            onClick={() => submitPrompt()}
          />
        </div>
      </div>
    </div>
  );
};
