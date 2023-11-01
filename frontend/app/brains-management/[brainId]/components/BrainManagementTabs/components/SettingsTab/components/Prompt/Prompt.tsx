import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { TextArea } from "@/lib/components/ui/TextArea";
import { SaveButton } from "@/shared/SaveButton";

import { usePrompt, UsePromptProps } from "../../hooks/usePrompt";
import { PublicPrompts } from "../PublicPrompts";

type PromptProps = {
  usePromptProps: UsePromptProps;
  isUpdatingBrain: boolean;
  hasEditRights: boolean;
};

export const Prompt = (props: PromptProps): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const { isUpdatingBrain, hasEditRights, usePromptProps } = props;

  const {
    pickPublicPrompt,
    register,
    submitPrompt,
    promptId,
    isRemovingPrompt,
    removeBrainPrompt,
  } = usePrompt(usePromptProps);

  return (
    <>
      {hasEditRights && <PublicPrompts onSelect={pickPublicPrompt} />}
      <Field
        label={t("promptName", { ns: "config" })}
        placeholder={t("promptNamePlaceholder", { ns: "config" })}
        autoComplete="off"
        className="flex-1"
        disabled={!hasEditRights}
        {...register("prompt.title")}
      />
      <TextArea
        label={t("promptContent", { ns: "config" })}
        placeholder={t("promptContentPlaceholder", { ns: "config" })}
        autoComplete="off"
        className="flex-1"
        disabled={!hasEditRights}
        {...register("prompt.content")}
      />
      {hasEditRights && (
        <div className="flex w-full justify-end py-4">
          <SaveButton handleSubmit={submitPrompt} />
        </div>
      )}
      {hasEditRights && promptId !== "" && (
        <Button
          disabled={isUpdatingBrain || isRemovingPrompt}
          onClick={() => void removeBrainPrompt()}
        >
          {t("removePrompt", { ns: "config" })}
        </Button>
      )}
    </>
  );
};
