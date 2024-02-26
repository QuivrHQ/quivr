import { UUID } from "crypto";

import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";

import styles from "./ModelSelection.module.scss";

import { useBrainFormState } from "../../hooks/useBrainFormState";

type ModelSelectionProps = {
  brainId: UUID;
  handleSubmit: (checkDirty: boolean) => Promise<void>;
  hasEditRights: boolean;
  accessibleModels: string[];
};

export const ModelSelection = (props: ModelSelectionProps): JSX.Element => {
  const { model, maxTokens, register } = useBrainFormState();
  const { handleSubmit, hasEditRights, accessibleModels } = props;

  const accessibleModelOptions = accessibleModels.map((accessibleModel) => {
    return { value: accessibleModel, label: accessibleModel };
  });

  return (
    <div className={styles.model_selection_wrapper}>
      <fieldset>
        <FieldHeader label="Model" iconName="robot" />
        <SingleSelector
          options={accessibleModelOptions}
          onChange={() => handleSubmit(false)}
          placeholder="Choose a model"
          selectedOption={{ value: model, label: model }}
          iconName="robot"
        />
      </fieldset>
      <fieldset>
        <FieldHeader label="Max tokens" iconName="hashtag" />
        <input
          type="range"
          min="10"
          max={defineMaxTokens(model)}
          value={maxTokens}
          disabled={!hasEditRights}
          {...register("maxTokens")}
        />
      </fieldset>
      {/* {hasEditRights && (
        <div>
          <SaveButton handleSubmit={handleSubmit} />
        </div>
      )} */}
    </div>
  );
};
