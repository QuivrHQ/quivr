import { UUID } from "crypto";
import { UseFormRegister } from "react-hook-form";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { TextArea } from "@/lib/components/ui/TextArea";
import { BrainConfig } from "@/lib/types/brainConfig";
import { SaveButton } from "@/shared/SaveButton";

import { PublicPrompts } from "../PublicPrompts";

type PromptProps = {
  brainId: UUID;
  pickPublicPrompt: ({
    title,
    content,
  }: {
    title: string;
    content: string;
  }) => void;
  removeBrainPrompt: () => Promise<void>;
  isUpdating: boolean;
  handleSubmit: (checkDirty: boolean) => Promise<void>;
  register: UseFormRegister<BrainConfig>;
  promptId?: string;
  hasEditRights: boolean;
};

export const Prompt = (props: PromptProps): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const {
    pickPublicPrompt,
    removeBrainPrompt,
    isUpdating,
    handleSubmit,
    register,
    hasEditRights,
    promptId,
  } = props;

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
          <SaveButton handleSubmit={handleSubmit} />
        </div>
      )}
      {hasEditRights && promptId !== "" && (
        <Button disabled={isUpdating} onClick={() => void removeBrainPrompt()}>
          {t("removePrompt", { ns: "config" })}
        </Button>
      )}
    </>
  );
};
