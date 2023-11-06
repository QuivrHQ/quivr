import { UUID } from "crypto";
import { UseFormRegister } from "react-hook-form";
import { useTranslation } from "react-i18next";

import Field from "@/lib/components/ui/Field";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { BrainConfig } from "@/lib/types/brainConfig";
import { SaveButton } from "@/shared/SaveButton";

type ModelSelectionProps = {
  brainId: UUID;
  temperature: number;
  maxTokens: number;
  model: "gpt-3.5-turbo" | "gpt-3.5-turbo-16k";
  handleSubmit: (checkDirty: boolean) => Promise<void>;
  register: UseFormRegister<BrainConfig>;
  hasEditRights: boolean;
  accessibleModels: string[];
};

export const ModelSelection = (props: ModelSelectionProps): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const {
    handleSubmit,
    register,
    temperature,
    maxTokens,
    model,
    hasEditRights,
    accessibleModels,
  } = props;

  return (
    <>
      <Field
        label={t("openAiKeyLabel", { ns: "config" })}
        placeholder={t("openAiKeyPlaceholder", { ns: "config" })}
        autoComplete="off"
        className="flex-1"
        disabled={!hasEditRights}
        {...register("openAiKey")}
      />
      <fieldset className="w-full flex flex-col mt-2">
        <label className="flex-1 text-sm" htmlFor="model">
          {t("modelLabel", { ns: "config" })}
        </label>
        <select
          id="model"
          disabled={!hasEditRights}
          {...register("model", {
            onChange: () => {
              void handleSubmit(false);
            },
          })}
          className="px-5 py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
        >
          {accessibleModels.map((availableModel) => (
            <option value={availableModel} key={availableModel}>
              {availableModel}
            </option>
          ))}
        </select>
      </fieldset>
      <fieldset className="w-full flex mt-4">
        <label className="flex-1" htmlFor="temp">
          {t("temperature", { ns: "config" })}: {temperature}
        </label>
        <input
          id="temp"
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={temperature}
          disabled={!hasEditRights}
          {...register("temperature")}
        />
      </fieldset>
      <fieldset className="w-full flex mt-4">
        <label className="flex-1" htmlFor="tokens">
          {t("maxTokens", { ns: "config" })}: {maxTokens}
        </label>
        <input
          type="range"
          min="10"
          max={defineMaxTokens(model)}
          value={maxTokens}
          disabled={!hasEditRights}
          {...register("maxTokens")}
        />
      </fieldset>
      {hasEditRights && (
        <div className="flex w-full justify-end py-4">
          <SaveButton handleSubmit={handleSubmit} />
        </div>
      )}
    </>
  );
};
