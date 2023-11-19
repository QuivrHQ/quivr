import { UUID } from "crypto";
import { useTranslation } from "react-i18next";

import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { SaveButton } from "@/shared/SaveButton";

import { useBrainFormState } from "../../hooks/useBrainFormState";

type ModelSelectionProps = {
  brainId: UUID;
  handleSubmit: (checkDirty: boolean) => Promise<void>;
  hasEditRights: boolean;
  accessibleModels: string[];
};

export const ModelSelection = (props: ModelSelectionProps): JSX.Element => {
  const { model, maxTokens, register } = useBrainFormState();
  const { t } = useTranslation(["translation", "brain", "config"]);
  const { handleSubmit, hasEditRights, accessibleModels } = props;

  return (
    <>
      
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
